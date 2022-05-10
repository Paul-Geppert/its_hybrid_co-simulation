#!/bin/sh

cd /

python3 -m converter -i i_conv_recv -c /converter/config.json

while true
do
    sleep 1
done
