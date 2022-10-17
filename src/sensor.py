from machine import Pin
from micropython import const

from debounce import PinDebouncer


"""
Any sub-second debounce period feels responsive enough for detecting a garage door so we choose a
reliable debounce period even though the datasheet says the operate and release times are 3.0 ms
"""
DEBOUNCE_PERIOD_MS: int = const(30)


def enable_sensor(sensor_pin_id: int, callback=None) -> Pin:
    # The GPIO pin must be pulled up externally
    switch = Pin(sensor_pin_id, Pin.IN, pull=None)
    _toggle_led(switch.value())

    def handle_switch_value_change(value: int) -> None:
        _toggle_led(value)
        if callback:
            callback(value)

    switch_debouncer = PinDebouncer(
        switch.value(),
        debounce_period_ms=DEBOUNCE_PERIOD_MS,
        callback=handle_switch_value_change,
    )
    switch.irq(
        switch_debouncer.handle_edge_trigger_irq,
        trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING,
    )

    return switch


def _toggle_led(value: int) -> None:
    Pin("LED", Pin.OUT, value=value)
