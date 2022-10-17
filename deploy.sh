#!/usr/bin/env bash

set -euo pipefail

pico_name="${PICO_BOARD:-pyboard}"
script_directory="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v rshell &> /dev/null; then
  echo 'rshell is not installed on this computer. Install it by following the instructions in the rshell repository at: https://github.com/dhylands/rshell'
  exit 1
fi

rshell rsync --mirror "$script_directory/src/" "/$pico_name"
rshell repl '~ import machine~ machine.soft_reset() ~'
