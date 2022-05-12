#!/bin/sh

echo "RSU started"

until ip a show v2x > /dev/null 2>&1
do
  echo 'waiting for network connection ...'
  sleep 1
done

exec "$@"
