#!/bin/bash

export DELAY_ROLE="RECEIVER"

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters" >&2
    exit 1
fi

TIMESTAMP=$1

until ip a show cv2x_c > /dev/null 2>&1
do
  echo 'waiting for network connection ...'
  sleep 1
done

curl -X GET localhost:13002/phy/metrics > simulation-logs/$TIMESTAMP/client.metrics.before.json
curl -X GET localhost:13002/phy/repo > simulation-logs/$TIMESTAMP/client.repo.before.json

ntpdate fritz.box > simulation-logs/$TIMESTAMP/client_clock_info_before_evaluation.log
ntpdate -q fritz.box >> simulation-logs/$TIMESTAMP/client_clock_info_before_evaluation.log

echo "Finished ntp update"

python3 -u -m delay -l simulation-logs/$TIMESTAMP/client.log

curl -X GET localhost:13002/phy/metrics > simulation-logs/$TIMESTAMP/client.metrics.after.json
curl -X GET localhost:13002/phy/repo > simulation-logs/$TIMESTAMP/client.repo.after.json
