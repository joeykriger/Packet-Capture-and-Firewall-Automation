**The User Report:**
> *"I can ping the Linux file server sometimes, but I can't consistently connect to the company's new application on port 8080."*

### The CompTIA Troubleshooting Methodology
As you work through this lab, document your actions using these six steps:
1. **Identify the problem:** *Windows can ping Linux, but cannot connect to port 8080.*
2. **Establish a theory of probable cause:** *Not layer 3 (ICMP succeeds) - must be a higher layer.*
3. **Test the theory to determine cause:** *Wrote three scripts for testing... Ran capture_launcher, but its coded to listen on interface 1 only (LabNet adpater is on interface 5). Corrected the script, reran it, and the capture shows ARP and ICMP traffic; Layers 2 & 3 are up. Must be Layer 4.*
4. **Establish a plan of action to resolve the problem and implement the solution:** *Disabled two outbound port 8080 firewall rules, and created an outbound allow rule for port 8080. Layer 4 now connectivity is now established.* 
5. **Verify full system functionality and implement preventive measures:** *Wireshark capture now confirms connectivity to the Linux server on port 8080. A new allow outbound port 8080 firewall rule has been added to WFD to prevent this issue from persistning.*
6. **Document findings, actions, and outcomes:** *See above documentation and screenshots folder.*
---

## Validation & Cleanup Checklist

- [X] Ubuntu server successfully receives the connection on `nc -l -p 8080`.
- [X] Windows VM successfully runs `auto_troubleshoot.py` with a PASS result.
- [X] CompTIA 6-step documentation is complete.
- [X] Remove static IPs and switch VirtualBox networking back to NAT (if desired for future labs).
- [X] Delete the Python-generated firewall rules to reset the environment.

---

# Portfolio Artifacts

### Screenshot Checklist for GitHub
Capture these to include in your repository's image folder:
- [X] Wireshark GUI showing successful ICMP but missing TCP SYN (The broken state).
- [X] Wireshark GUI showing a successful 3-way TCP handshake (The fixed state).
- [X] The output of your `auto_troubleshoot.py` script showing a PASS.