#!/bin/bash
if pgrep -f -x "python casa.py" > /dev/null; then
    echo "casa.py already started"
else
    echo "starting casa.py"
    cd /home/pi/casanova/casa2/; python casa.py
fi
