#!/bin/bash
set -e

cd /home/container

export PATH=/opt/venv/bin:/home/container/.local/bin:$PATH
export PYTHONPATH=/home/container/.local/lib/python3.12/site-packages:$PYTHONPATH

STARTUP_PROCESSED=$(echo "${STARTUP}" | sed -e 's/{{/${/g' -e 's/}}/}/g')
echo "Starting bot with command: ${STARTUP_PROCESSED}"

eval "${STARTUP_PROCESSED}"
