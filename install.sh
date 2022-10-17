#!/usr/bin/env bash

set -euo pipefail

script_directory="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
lib_directory="$script_directory/src/lib"

mkdir -p "$lib_directory"

# microdot 1.2.0
echo "Downloading microdot..."
curl --silent --output-dir "$lib_directory" \
  --remote-name https://raw.githubusercontent.com/miguelgrinberg/microdot/v1.2.0/src/microdot.py \
  --remote-name https://raw.githubusercontent.com/miguelgrinberg/microdot/v1.2.0/src/microdot_asyncio.py #\
  # --remote-name https://raw.githubusercontent.com/miguelgrinberg/microdot/v1.2.0/src/microdot_asyncio_websocket.py \
  # --remote-name https://raw.githubusercontent.com/miguelgrinberg/microdot/v1.2.0/src/microdot_websocket.py

# mqtt_as 0.7.0
echo "Downloading mqtt_as..."
curl --silent --output-dir "$lib_directory" \
  --remote-name https://raw.githubusercontent.com/peterhinch/micropython-mqtt/000b67778bf0a9308ac99c7ce2b54c8a1c4ce23c/mqtt_as/mqtt_as.py
