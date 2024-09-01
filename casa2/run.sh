#!/bin/bash
if pgrep -x "run.sh" > /dev/null; then
    echo "run.sh already started"
else
    cd /home/pi/casanova/casa2/; python casa.py
fi
