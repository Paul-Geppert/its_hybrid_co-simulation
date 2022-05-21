#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters" >&2
    exit 1
fi

TIMESTAMP=$1

LOG_LEVEL="info"

LOG_FILE="${DELAY_ROLE}.log"
MAC_PCAP_FILE="${DELAY_ROLE}_mac.pcap"
NAS_PCAP_FILE="${DELAY_ROLE}_nas.pcap"
DATADIR="simulation-logs/${TIMESTAMP}"
LOG_FILE="${DATADIR}/${LOG_FILE}"
MAC_PCAP_FILE="${DATADIR}/${MAC_PCAP_FILE}"
NAS_PCAP_FILE="${DATADIR}/${NAS_PCAP_FILE}"

if [ "$DELAY_ROLE" = "SENDER" ]; then
    SIDELINK_MASTER="1"
    SIDELINK_ID="1"
    DEVICE_ARGS="type=b200,serial=320F319"
    IF_NAME="cv2x_m"
else
    SIDELINK_MASTER="0"
    SIDELINK_ID="2"
    DEVICE_ARGS="type=b200,serial=320F331"
    IF_NAME="cv2x_c"
fi

sidelink/build/srssl/src/srssl ./sdr_evaluation.conf --expert.phy.sidelink_id $SIDELINK_ID --expert.phy.sidelink_master $SIDELINK_MASTER --log.filename $LOG_FILE --log.all_level $LOG_LEVEL --pcap.enable 1 --pcap.filename $MAC_PCAP_FILE --pcap.nas_enable 1 --pcap.nas_filename $NAS_PCAP_FILE --rf.device_args $DEVICE_ARGS --gw.tun_dev_name $IF_NAME
