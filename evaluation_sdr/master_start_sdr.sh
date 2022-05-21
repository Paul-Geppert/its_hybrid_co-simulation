#!/bin/bash
export DELAY_ROLE="SENDER"

TIMESTAMP=`date +"%Y-%m-%d_%H-%M-%S"`
DATA_DIR="simulation-logs/${TIMESTAMP}"

mkdir -p $DATA_DIR

echo DATA_DIR is $DATA_DIR

./start_sdr.sh $DATA_DIR
