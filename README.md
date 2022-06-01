# ITS Hybrid Co-Simulation

This repository contains the code for my master thesis "Integration of the C-V2X radio technology into hybrid testbeds for co-simulation in the context of intelligent transportation systems".

The three submodules are included:

- marvis: hybrid co-simulation
- ns-3_-c-v2x: ns-3 network simulator with C-V2X support
- sidelink: C-V2X framework from HHI for Ettus Research USRP B210

Additional content:

- evaluation_latency_ns3: Code to analyze latency and PDR for C-V2X in ns-3_c-v2x for different distances and transmit powers
- evaluation_sdr: Code to analyze latency and PDR for C-V2X when using SDRs and HHI-Sidelink
- scenario: Run the DiAK-Scenario presented in the master thesis

For more information check the README.md of the submodules or directories.
