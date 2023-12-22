import json


def publish_homeassistant_discovery_message(
    mqtt, device_id: str, state_topic: str
) -> None:
    mqtt.publish(
        f"homeassistant/binary_sensor/{device_id}/config",
        json.dumps(
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


def publish_sensor_state_message(mqtt, state_topic: str, sensor_state: bool) -> None:
    mqtt.publish(
        state_topic,
        "ON" if sensor_state else "OFF",
        retain=True,
        qos=1,
    )
