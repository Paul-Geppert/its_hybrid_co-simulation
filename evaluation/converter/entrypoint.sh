#!/bin/sh

# Interface to receive ITS-G5 messages from
until ip a show i_conv_recv > /dev/null 2>&1
do
  echo 'waiting for network connection i_conv_recv ...'
  sleep 1
done

# Interface to send C-V2X messages to
until ip a show i_conv_send > /dev/null 2>&1
do
  echo 'waiting for network connection i_conv_send ...'
  sleep 1
done

# Interface to send converted V2X messages to MQTT
until ip a show i_conv_eth > /dev/null 2>&1
do
  echo 'waiting for network connection i_conv_eth ...'
  sleep 1
done

exec "$@"
