import os

import storage

if os.getenv("LOG_FILE"):
  # Allow CircuitPython to write to its flash storage
  # https://learn.adafruit.com/circuitpython-essentials/circuitpython-storage
  storage.remount("/", readonly=False, disable_concurrent_write_protection=True)
