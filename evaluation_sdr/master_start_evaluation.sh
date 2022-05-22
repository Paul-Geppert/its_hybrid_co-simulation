#!/bin/bash

export DELAY_ROLE="SENDER"

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters" >&2
    exit 1
fi

TIMESTAMP=$1

until ip a show cv2x_m > /dev/null 2>&1
do
  echo 'waiting for network connection ...'
  sleep 1
done

curl -X GET localhost:13001/phy/metrics > simulation-logs/$TIMESTAMP/master.metrics.before.json
curl -X GET localhost:13001/phy/repo > simulation-logs/$TIMESTAMP/master.repo.before.json

ntpdate fritz.box > simulation-logs/$TIMESTAMP/master_clock_info_before_evaluation.log
ntpdate -q fritz.box >> simulation-logs/$TIMESTAMP/master_clock_info_before_evaluation.log

python3 -u -m delay -l simulation-logs/$TIMESTAMP/master.log

curl -X GET localhost:13001/phy/metrics > simulation-logs/$TIMESTAMP/master.metrics.after.json
curl -X GET localhost:13001/phy/repo > simulation-logs/$TIMESTAMP/master.repo.after.json
