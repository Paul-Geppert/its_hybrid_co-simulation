#!/bin/bash
export DELAY_ROLE="RECEIVER"

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

./start_sdr.sh $DATA_DIR
