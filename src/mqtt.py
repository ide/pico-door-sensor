import json

from mqtt_as import MQTTClient, config as mqtt_default_client_config


def mqtt_client_config(config: dict) -> dict:
    mqtt_config = config.get("mqtt", {})
    wifi_config = config.get("wifi", {})
    return dict(
        mqtt_default_client_config,
        ssid=wifi_config.get("ssid"),
        wifi_pw=wifi_config.get("password"),
        server=mqtt_config.get("hostname"),
        user=mqtt_config.get("username"),
        password=mqtt_config.get("password"),
    )


async def publish_homeassistant_discovery_message(
    mqtt: MQTTClient, device_id: str, state_topic: str
) -> None:
    await mqtt.publish(
        f"homeassistant/binary_sensor/{device_id}/config",
        mqtt_json_message(
            {
                "unique_id": device_id,
                "name": "Garage Door",
                "object_id": "garage_door",
                "device": {
                    "name": "Door Sensor",
                    "identifiers": [device_id],
                    "model": "Raspberry Pi Pico W Door Sensor",
                    "manufacturer": "Raspberry Pi",
                    "suggested_area": "garage",
                },
                "device_class": "garage_door",
                "state_topic": state_topic,
            }
        ),
        retain=True,
    )


def mqtt_string_message(string: str) -> bytes:
    return bytes(string, "utf-8")


def mqtt_json_message(object: dict) -> bytes:
    return bytes(json.dumps(object), "utf-8")
