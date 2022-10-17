import gc
import json
from machine import reset, unique_id
from micropython import alloc_emergency_exception_buf, const
import rp2
from sys import print_exception
import uasyncio as asyncio

from mqtt_as import MQTTClient

from mqtt import (
    mqtt_client_config,
    mqtt_json_message,
    mqtt_string_message,
    publish_homeassistant_discovery_message,
)
from sensor import enable_sensor

DOOR_SWITCH_GPIO: int = const(22)


async def main() -> None:
    gc.collect()

    # Allocate a small amount of memory to capture stack traces within interrupt handlers
    alloc_emergency_exception_buf(100)

    # Read in the global configuration from the filesystem
    config = load_config()

    # Use the Wi-Fi channels of the configured country or default to a worldwide subset
    wifi_config = config.get("wifi", {})
    country = wifi_config.get("country")
    if country is not None:
        rp2.country(country)

    # The MQTT client also handles connecting to the configured Wi-Fi network
    mqtt = MQTTClient(mqtt_client_config(config))
    try:
        await mqtt.connect()
    except OSError as e:
        print("Failed to connect to the MQTT broker")
        print_exception(e)
        reset()

    # Announce this device to Home Assistant
    # https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery
    mqtt_device_id = unique_id().hex()
    mqtt_state_topic = f"door/{mqtt_device_id}/state"
    await publish_homeassistant_discovery_message(
        mqtt, mqtt_device_id, mqtt_state_topic
    )

    # Start listening to the garage door sensor
    loop = asyncio.get_event_loop()

    def publish_sensor_value(value: int) -> None:
        print(
            f"The door is open (sensor value = {value})"
            if value is 0
            else f"The door is closed (sensor value = {value})"
        )
        loop.run_until_complete(
            mqtt.publish(
                mqtt_state_topic,
                mqtt_string_message("ON" if value is 0 else "OFF"),
                retain=True,
                qos=1,
            )
        )

    sensor_pin = enable_sensor(
        config.get("sensor_pin", DOOR_SWITCH_GPIO), publish_sensor_value
    )
    publish_sensor_value(sensor_pin.value())

    gc.collect()


def load_config() -> dict:
    with open("config.json") as config_file:
        return json.load(config_file)


asyncio.run(main())
