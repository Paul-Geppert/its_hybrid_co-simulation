# Measuring c-v2x_ns-3

## What will be measured

- Delay between sending and receiving a message
- Number of sent messages vs number of received messages

## Configuration details

`evaluation_delay_ns3.py` has two arrays for distance between receiver and transmitter and the `tx_power` used. All possible combinations will be executed in a simple scenario and the metrics will be logged in files.

`delay_evaluator.py` will gather and evaluate the data.
