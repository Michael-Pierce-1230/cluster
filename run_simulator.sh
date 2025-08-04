#!/bin/bash

# Navigate to the project root (optional if already there)
#
#set PYTHONPATH to current directory so 'src is importable
export PYTHONPATH=.

python3 src/server/can_bus/canbus_simulator.py
