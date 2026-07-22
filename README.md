# Packet Capture & Firewall Automation Lab

## Overview
This repository contains a hands-on home lab project demonstrating network troubleshooting, packet analysis, and task automation. Designed around a realistic Help Desk / Junior System Administrator scenario, this project applies the CompTIA troubleshooting methodology to diagnose and resolve a simulated connectivity issue across the OSI model.

## Skills Demonstrated
- **Networking:** TCP/IP model, OSI model analysis, static IP configuration, ICMP, and TCP handshakes.
- **Packet Analysis:** Traffic capture and network analysis using Wireshark and `tshark`.
- **Automation:** Python 3 scripting (utilizing standard libraries like `subprocess` and `os`) to automate network testing, packet captures, and data parsing.
- **Systems Administration:** Windows Defender Firewall management and PowerShell command execution via Python.
- **Methodology:** Practical application of the 6-step CompTIA Troubleshooting Methodology.

## Tools & Environment
- **Hypervisor:** Oracle VirtualBox (Isolated `LabNet` Internal Network)
- **Virtual Machines:** Windows 11 Home & Ubuntu Linux Desktop
- **Languages:** Python 3.13, PowerShell, Bash
- **Software:** Wireshark, Npcap, Netcat

## Repository Structure
```text
Packet-Capture-Firewall-Automation-Lab/
├── README.md                                  # Project overview (This file)
├── Packet_Capture_Firewall_Automation_Lab.md  # Detailed step-by-step scenario guide
├── troubleshooting/                           # Checklists
├── python/                                    # Python automation scripts
│   ├── connectivity_tester.py
│   ├── capture_launcher.py
│   ├── capture_parser.py
│   ├── firewall_audit.py
│   ├── firewall_manager.py
│   └── auto_troubleshoot.py
├── screenshots/                               # Wireshark and terminal output evidence
└── captures/                                  # Sample .pcapng files generated during the lab
```

## Reviewing the Project
To review this lab and its deliverables:
1. Read the full scenario, setup instructions, and troubleshooting steps in the **[Lab Scenario Guide](Packet_Capture_Firewall_Automation_Lab.md)**.
2. Review the Python scripts in the `python/` directory to see the automation and system administration logic.
3. Check the `screenshots/` folder for visual validation of the broken state, the network traffic analysis, and the final resolved state.
