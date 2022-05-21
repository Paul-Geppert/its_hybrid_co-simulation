#!/bin/bash
export DELAY_ROLE="SENDER"

TIMESTAMP=`date +"%Y%m%d%H%M%Sh"`

echo TIMESTAMP is $TIMESTAMP

./start_sdr.sh $TIMESTAMP
