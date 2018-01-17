#!/bin/bash

set -e

SYSTEM=`uname -s`

if [ "${SYSTEM}" == "Linux" ]; then
    ./halite.linux -d "240 160" "python3 settler.py" "python3 MyBot.py"
elif [ "${SYSTEM}" == "Darwin" ]; then
    ./halite.macos -d "240 160" "python3 settler.py" "python3 MyBot.py"
else
    echo "No such executable for system ${SYSTEM} found."
    exit 1;
fi
