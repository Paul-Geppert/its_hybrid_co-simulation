#!/bin/bash
export LATENCY_ROLE="RECEIVER"

if [ "$#" -ne 2 ]; then
    echo "Error: Need DISTANCE and GAIN parameter." >&2
    exit 1
fi

DISTANCE=$1
GAIN=$2

TIMESTAMP=`date +"%Y-%m-%d_%H-%M-%S_dist_${DISTANCE}_gain_${GAIN}"`
DATA_DIR="simulation-logs/${TIMESTAMP}"

mkdir -p $DATA_DIR

echo DATA_DIR is $DATA_DIR

ntpdate fritz.box > $DATA_DIR/client_clock_info_before_sdr.log
ntpdate -q fritz.box >> $DATA_DIR/client_clock_info_before_sdr.log

echo "Finished ntp update"

./start_sdr.sh $DATA_DIR
