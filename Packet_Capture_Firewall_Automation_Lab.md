# Packet Capture and Firewall Automation Lab

## Executive Summary
This lab simulates a realistic Help Desk/Junior System Administrator scenario. It combines foundational networking concepts (A+/Network+), CompTIA troubleshooting methodologies, packet analysis (Wireshark/tshark), and beginner-level Python scripting. You will investigate a connectivity issue, analyze traffic across the OSI model, and automate Windows Firewall management using Python's standard library.

## Learning Objectives
- Map network connectivity issues to specific layers of the OSI and TCP/IP models.
- Apply the 6-step CompTIA Troubleshooting Methodology to a realistic ticket.
- Perform network traffic capture and analysis using Wireshark and `tshark`.
- Write beginner-friendly Python scripts to automate ping tests, packet captures, and Windows Defender Firewall rules.

## Network Topology & Environment
**Hypervisor:** Oracle VirtualBox
**Network Isolation:** Internal Network only (`LabNet`) - The host machine is completely isolated.

```text
      [ LabNet - VirtualBox Internal Network ]
                   |
    +--------------+---------------+
    |                              |
[ Windows 11 Home VM ]     [ Ubuntu Linux VM ]
    192.168.10.20             192.168.10.10
    (Python 3.13,             (Application/File Server)
    Wireshark, Npcap)
```

## Prerequisites
- VirtualBox installed with two VMs: Windows 11 Home and Ubuntu Linux Desktop.
- Both VMs attached to the VirtualBox Internal Network named `LabNet`.
- Windows 11 VM: Python 3.13 installed (added to PATH).
- Windows 11 VM: Wireshark installed (with `tshark` and Npcap).

---

## Phase 1: Environment Configuration & Intentional Sabotage Setup

Before beginning the troubleshooting scenario, you must configure the environment and set up the "sabotage" to simulate the user's issue.

### 1. Static IP Configuration
1. **Ubuntu VM:** Configure the primary network interface with static IP `192.168.10.10`, subnet mask `255.255.255.0`.
2. **Windows 11 VM:** Configure the primary network interface with static IP `192.168.10.20`, subnet mask `255.255.255.0`.

### 2. The Sabotage (Pre-Lab Setup)
To create the scenario, we need to intentionally break the configuration. 
**On the Ubuntu VM:**
Open a terminal and start a dummy application service that listens on port 8080:
```bash
# Simulates the company's new application
nc -l -p 8080
```

**On the Windows 11 VM:**
Open PowerShell **as Administrator** and run the following commands to create a complex, broken firewall state:
```powershell
# 1. Block outbound TCP traffic destined for remote port 8080
New-NetFirewallRule -DisplayName "Block_App_Port" -Direction Outbound -RemotePort 8080 -Protocol TCP -Action Block

# 2. Misleading allow rule (applies to UDP instead of TCP on remote port 8080)
New-NetFirewallRule -DisplayName "Allow_Company_App" -Direction Outbound -RemotePort 8080 -Protocol UDP -Action Allow

# 3. Incorrect inbound rule (Inbound rules correctly use LocalPort for listening ports)
New-NetFirewallRule -DisplayName "Inbound_App_Traffic" -Direction Inbound -LocalPort 80 -Protocol TCP -Action Block
```

---

## Phase 2: The Help Desk Ticket

**The User Report:**
> *"I can ping the Linux file server sometimes, but I can't consistently connect to the company's new application on port 8080."*

### The CompTIA Troubleshooting Methodology
As you work through this lab, document your actions using these six steps:
1. **Identify the problem:** (What is broken? Gather information, duplicate the problem if possible.)
2. **Establish a theory of probable cause:** (Question the obvious. Is it Layer 1, 2, 3, or 4? Is it the firewall?)
3. **Test the theory to determine cause:** (Use your Python scripts and Wireshark to test.)
4. **Establish a plan of action to resolve the problem and implement the solution:** (Fix the firewall/scripts.)
5. **Verify full system functionality and implement preventive measures:** (Test again.)
6. **Document findings, actions, and outcomes:** (Complete your Markdown notes.)

---

## Phase 3: Python Automation (Building Your Tools)

Instead of using standard GUI tools, you will build beginner-friendly Python scripts to troubleshoot this ticket. **Use only Python's standard library (`subprocess`, `os`, `sys`, `time`, `re`).**

### Script 1: Connectivity Tester (`connectivity_tester.py`)
**Goal:** Automate pinging the Ubuntu server to test Layer 3 connectivity.
**Task:** Write a script using `subprocess.run` to execute the `ping` command to `192.168.10.10` and print the output. 
*OSI Layer: 3 (Network - ICMP)*

```python
import subprocess

target_ip = "192.168.10.10"
print(f"Testing Layer 3 connectivity to {target_ip}...")

result = subprocess.run(['ping', '-n', '4', target_ip], capture_output=True, text=True)

print(result.stdout)
if result.returncode == 0:
    print("Ping successful! Layer 3 is up.")
else:
    print("Ping failed! Check Layer 3 connectivity.")
```

### Script 2: Packet Capture Launcher (`capture_launcher.py`)
**Goal:** Automate `tshark` to capture traffic for 10 seconds.
**Task:** Write a script that uses `subprocess` to call `tshark.exe`.
**Intentional Sabotage/Bug:** In your script, hardcode the interface index to `-i 1`. 
*Troubleshooting checkpoint: Does index 1 map to your LabNet adapter, or a loopback/disconnected adapter? You will need to run `tshark -D` in your terminal, find the correct index, and fix your Python script!*

```python
import subprocess

# Intentional Sabotage: Interface 1 may not be the correct 'LabNet' adapter.
# You will need to run 'tshark -D' in terminal to find the right index and update this variable.
interface = "1"
duration = "10"
output_file = "capture.pcapng"

print(f"Starting packet capture on interface {interface} for {duration} seconds...")

tshark_cmd = [
    'tshark', 
    '-i', interface, 
    '-a', f'duration:{duration}', 
    '-w', output_file
]

try:
    subprocess.run(tshark_cmd, check=True)
    print(f"Capture complete. Saved to {output_file}")
except FileNotFoundError:
    print("Error: tshark not found. Ensure Wireshark is installed and added to your PATH.")
except subprocess.CalledProcessError:
    print("Error: Capture failed. Are you running as Administrator? Is the interface index correct?")
```

### Script 3: Packet Summary Parser (`capture_parser.py`)
**Goal:** Read a `.pcapng` file and summarize the protocols.
**Task:** Use `subprocess` to run `tshark.exe -r capture.pcapng -q -z io,phs` and print the output so you can see if TCP/8080 traffic is actually leaving the machine.

```python
import subprocess

capture_file = "capture.pcapng"
print(f"Analyzing {capture_file} for protocol hierarchy statistics...")

tshark_cmd = [
    'tshark',
    '-r', capture_file,
    '-q',
    '-z', 'io,phs'
]

try:
    result = subprocess.run(tshark_cmd, capture_output=True, text=True, check=True)
    print("\n--- Protocol Hierarchy Statistics ---")
    print(result.stdout)
except FileNotFoundError:
    print("Error: tshark not found.")
except subprocess.CalledProcessError:
    print(f"Error reading file. Ensure '{capture_file}' exists in the directory.")
```

---

## Phase 4: OSI Analysis & Wireshark Exercises

With your scripts built, test the user's claim:
1. Run `connectivity_tester.py`. (It should succeed. Layer 3 is up.)
2. Open a web browser or use PowerShell (`Test-NetConnection 192.168.10.10 -Port 8080`) to test the application. (It will fail).
3. Start `capture_launcher.py`. While it runs, attempt the connection to 8080 again.
4. Open the resulting `.pcapng` in the Wireshark GUI.

**Troubleshooting Prompts:**
*   **Are you capturing on the right interface:** Run tshark -D and confirm that the interface matches what is on the capture_launcher.py sript.
*   **Layer 3 vs Layer 4:** Is there an ARP request/reply? Is there an ICMP echo request/reply? This confirms Layers 2 and 3 are working. 
*   **The TCP Handshake:** Filter your capture by `tcp.port == 8080`. Do you see a SYN packet leaving the Windows VM? 
*   *If no SYN packet is on the wire, but Layer 3 works, what component on the host OS drops traffic before it hits the virtual wire?* (Answer: Host Firewall).

---

## Phase 5: Firewall Automation & Resolution

### Script 4: Firewall Audit Script (`firewall_audit.py`)
**Goal:** Find the sabotage. 
**Task:** Write a Python script that runs `powershell -Command "Get-NetFirewallRule | Where-Object {$_.LocalPort -eq '8080'}"` via `subprocess`. 
*Identify the overly broad deny rule and the misleading UDP allow rule.*

```python
import subprocess

print("Auditing Windows Defender Firewall for rules affecting port 8080...")

# Check both RemotePort and LocalPort so no rules are missed
ps_cmd = "Get-NetFirewallRule | Where-Object {$_.RemotePort -eq '8080' -or $_.LocalPort -eq '8080'} | Select-Object DisplayName, Direction, Action, Protocol | Format-Table"

result = subprocess.run(['powershell', '-Command', ps_cmd], capture_output=True, text=True)

print("\n--- Firewall Audit Results ---")
if result.stdout.strip():
    print(result.stdout)
else:
    print("No rules found affecting port 8080.")
```

### Script 5: Firewall Rule Creator (`firewall_manager.py`)
**Goal:** Automate the fix.
**Task:** Write a script that executes PowerShell commands to:
1. Remove/Disable the `Block_App_Port` rule.
2. Remove/Disable the `Allow_Company_App` UDP rule.
3. Add a new, correct rule: `Allow_Ubuntu_App`, Direction: Outbound, Protocol: TCP, Port: 8080, Action: Allow.

```python
import subprocess

print("Implementing firewall resolutions...")

commands = [
    # 1. Disable the overly broad deny rule
    "Disable-NetFirewallRule -DisplayName 'Block_App_Port' -ErrorAction SilentlyContinue",
    
    # 2. Disable the misleading UDP allow rule
    "Disable-NetFirewallRule -DisplayName 'Allow_Company_App' -ErrorAction SilentlyContinue",
    
    # 3. Add the correct outbound rule for TCP 8080
    "New-NetFirewallRule -DisplayName 'Allow_Ubuntu_App' -Direction Outbound -RemotePort 8080 -Protocol TCP -Action Allow"
]

for cmd in commands:
    print(f"Executing: {cmd.split('-DisplayName')[0].strip()}...")
    result = subprocess.run(['powershell', '-Command', cmd], capture_output=True, text=True)
    if result.returncode == 0:
        print(" -> Success.")
    else:
        print(" -> Action failed, or rule already modified.")

print("Firewall rules updated successfully.")
```

### Script 6: Automated Troubleshooting Script (`auto_troubleshoot.py`)
**Goal:** The final verification step (Step 5 of CompTIA methodology).
**Task:** Combine your tools. Write a script that:
1. Pings `192.168.10.10`.
2. Tests TCP/8080 (Using PowerShell `Test-NetConnection -ComputerName 192.168.10.10 -Port 8080 -InformationLevel Quiet` via `subprocess`).
3. Prints a clear "PASS" or "FAIL" report for both Layer 3 and Layer 4.

```python
import subprocess

target_ip = "192.168.10.10"
port = "8080"

print(f"--- Automated Troubleshooting Report for {target_ip} ---")

# Verify Layer 3 (ICMP)
print("1. Testing Layer 3 (ICMP)...")
ping_result = subprocess.run(['ping', '-n', '1', target_ip], capture_output=True, text=True)

if ping_result.returncode == 0:
    print("   [PASS] Layer 3 connectivity established.")
else:
    print("   [FAIL] Layer 3 connectivity failed.")

# Verify Layer 4 (TCP)
print(f"2. Testing Layer 4 (TCP Port {port})...")
ps_cmd = f"Test-NetConnection -ComputerName {target_ip} -Port {port} -InformationLevel Quiet"
tcp_result = subprocess.run(['powershell', '-Command', ps_cmd], capture_output=True, text=True)

if "True" in tcp_result.stdout:
    print(f"   [PASS] Layer 4 connectivity established on port {port}.")
else:
    print(f"   [FAIL] Layer 4 connectivity failed.")

print("--- Report Complete ---")
```

---

## Validation & Cleanup Checklist

- [ ] Ubuntu server successfully receives the connection on `nc -l -p 8080`.
- [ ] Windows VM successfully runs `auto_troubleshoot.py` with a PASS result.
- [ ] CompTIA 6-step documentation is complete.
- [ ] Remove static IPs and switch VirtualBox networking back to NAT (if desired for future labs).
- [ ] Delete the Python-generated firewall rules to reset the environment.

---

## Portfolio Artifacts

### Screenshot Checklist for GitHub
Capture these to include in your repository's image folder:
1. Wireshark GUI showing successful ICMP but missing TCP SYN (The broken state).
2. Wireshark GUI showing a successful 3-way TCP handshake (The fixed state).
3. The output of your `auto_troubleshoot.py` script showing a PASS.

