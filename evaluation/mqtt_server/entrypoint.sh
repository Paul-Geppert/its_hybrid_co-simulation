#!/bin/sh

until ip a show i_mqtt &> /dev/null
do
  echo 'waiting for network connection ...'
  sleep 1
done

exec "$@"
