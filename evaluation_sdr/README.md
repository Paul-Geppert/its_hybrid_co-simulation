# Evaluation of C-V2X via SDR

This evaluation does not require Marvis but evaluates the SDRs only.
To create pyhsical distance between the SDRs you could use two computers, one running as Master, one as Client.
When measuring latency, these computers need have synchronized clocks. This evaluation uses a NTP server to synchronize.
The NTP server is a local server to ensure best results and is located at `fritz.box`. Change this address with an appropriate NTP server which suits your needs best.

**Please make sure the frequency you use is legal to use for you and does not interfere with other signals and devices.**
You can configure the settings in `sdr_evaluation.conf`.

## What is measured

We measure the same information and metrics as in `evaluation_latency_ns3`. Please check the README there to learn more.
We log in the same format to be able use the same results analyzer.
