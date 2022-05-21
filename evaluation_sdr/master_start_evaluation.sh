#!/bin/bash

export DELAY_ROLE="SENDER"

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters" >&2
    exit 1
fi

TIMESTAMP=$1

until ip a show cv2x_m > /dev/null 2>&1
do
  echo 'waiting for network connection ...'
  sleep 1
done

python3 -m delay -u -l simulation-logs/$TIMESTAMP/master.log
