from machine import Pin, Timer
from micropython import const, schedule
from uasyncio import ThreadSafeFlag


class PinDebouncer:
    DEFAULT_DEBOUNCE_PERIOD_MS: int = const(10)

    def __init__(
        self,
        initial_value: int,
        debounce_period_ms: int = DEFAULT_DEBOUNCE_PERIOD_MS,
        callback=None,
    ) -> None:
        self.value = initial_value
        self._value_change_flag = ThreadSafeFlag()
        self._value_change_callback = callback
        self._debounce_timer = Timer()
        self._debounce_period_ms = debounce_period_ms

        # The pin's value at the time of the last edge trigger, only to be accessed during an IRQ
        self._irq_pin_value = initial_value

        # Eagerly bind instance methods so memory is not allocated during an IRQ
        self._debounce_timer_isr = self._handle_debounce_timer_irq
        self._set_value = self.set_value

    def handle_edge_trigger_irq(self, pin: Pin) -> None:
        """
        Handles a change in the switch pin's state, triggered by either a rising or falling edge.
        This function runs inside an IRQ. The switch is debounced using a timer mainly to filter
        noise from the reed switch.
        """
        self._irq_pin_value = pin.value()

        # If there is a pending timer due to an earlier edge trigger, setting the timer here cancels
        # the previous timer and schedules a new one
        self._debounce_timer.init(
            mode=Timer.ONE_SHOT,
            period=self._debounce_period_ms,
            callback=self._debounce_timer_isr,
        )

    def _handle_debounce_timer_irq(self, timer: Timer) -> None:
        """
        Handles the debounce timer when enough time has elapsed since the last edge trigger IRQ.
        This function itself runs inside the timer's IRQ.
        """
        schedule(self._set_value, self._irq_pin_value)

    def set_value(self, value: int) -> None:
        """
        Sets the switch state to the given pin's current value. This function runs outside of an
        IRQ.
        """
        if value == self.value:
            return

        self.value = value
        self._value_change_flag.set()

        if self._value_change_callback is not None:
            self._value_change_callback(value)

    async def wait_for_toggle(self) -> int:
        """
        A coroutine that waits for the pin to change value and returns the new, debounced value of
        the pin. Only one task at a time may await this coroutine.
        """
        self._value_change_flag.clear()
        await self._value_change_flag.wait()
        return self.value
