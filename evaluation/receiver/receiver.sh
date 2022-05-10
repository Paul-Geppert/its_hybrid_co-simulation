#!/bin/sh

while true
do
  echo 'subscribing to spat/hpi ...'
  mosquitto_sub -h mqtt_server -p 1883 -u test_user -P 'pwd' -t spat/thesis
  sleep 1
done
