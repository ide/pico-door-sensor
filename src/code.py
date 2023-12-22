import binascii
import os
import time
import traceback

import board
import digitalio
import microcontroller
import socketpool
import supervisor
import wifi

import adafruit_debouncer
import adafruit_logging
import adafruit_minimqtt.adafruit_minimqtt as adafruit_minimqtt

from logging import create_logger
from mqtt import publish_homeassistant_discovery_message, publish_sensor_state_message


def main(logger: adafruit_logging.Logger) -> None:
    led = digitalio.DigitalInOut(board.LED)
    led.switch_to_output()

    switch_io = digitalio.DigitalInOut(board.GP22)
    # GPIO 22 has a pull-up resistor so we don't pull it up in code
    switch_io.switch_to_input()
    switch = adafruit_debouncer.Debouncer(switch_io)

    # The switch is open when the door is closed
    led.value = not switch.value

    # Connect to the Wi-Fi network
    logger.info("Connecting to the local Wi-Fi network...")
    wifi.radio.hostname = os.getenv("WIFI_HOSTNAME")
    wifi.radio.connect(
        os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD")
    )
    logger.info(
        "Connected to the local network: IP address = %s, router = %s, DNS server %s",
        wifi.radio.ipv4_address,
        wifi.radio.ipv4_gateway,
        wifi.radio.ipv4_dns,
    )
    pool = socketpool.SocketPool(wifi.radio)

    # Connect to the MQTT broker
    logger.info("Connecting to the MQTT broker...")
    mqtt = adafruit_minimqtt.MQTT(
        broker=os.getenv("MQTT_HOSTNAME"),
        username=os.getenv("MQTT_USERNAME"),
        password=os.getenv("MQTT_PASSWORD"),
        is_ssl=False,
        socket_pool=pool,
    )
    mqtt.logger = logger
    mqtt.connect()
    logger.info("Connected to the MQTT broker")

    mqtt_device_id = binascii.hexlify(microcontroller.cpu.uid).decode("utf-8")
    mqtt_state_topic = f"door/{mqtt_device_id}/state"
    publish_homeassistant_discovery_message(mqtt, mqtt_device_id, mqtt_state_topic)
    publish_sensor_state_message(mqtt, mqtt_state_topic, not switch.value)
    logger.info("Advertised Home Assistant discovery message and current door state")

    logger.info("Monitoring door sensor...")
    while True:
        switch.update()
        mqtt.loop()

        if switch.rose or switch.fell:
            is_door_open = not switch.value
            logger.info(
                "Detected the door open" if is_door_open else "Detected the door closed"
            )
            led.value = is_door_open
            publish_sensor_state_message(mqtt, mqtt_state_topic, is_door_open)


logger = create_logger()

try:
    main(logger)
except Exception as exception:
    logger.critical("%s", "".join(traceback.format_exception(exception, limit=8)))
    time.sleep(10)
    if supervisor.runtime.usb_connected:
        supervisor.reload()
    else:
        microcontroller.reset()
