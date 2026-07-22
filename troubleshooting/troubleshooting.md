**The User Report:**
> *"I can ping the Linux file server sometimes, but I can't consistently connect to the company's new application on port 8080."*

### The CompTIA Troubleshooting Methodology
As you work through this lab, document your actions using these six steps:
1. **Identify the problem:** 
2. **Establish a theory of probable cause:** 
3. **Test the theory to determine cause:** 
4. **Establish a plan of action to resolve the problem and implement the solution:** 
5. **Verify full system functionality and implement preventive measures:** 
6. **Document findings, actions, and outcomes:** 
---

## Validation & Cleanup Checklist

- [ ] Ubuntu server successfully receives the connection on `nc -l -p 8080`.
- [ ] Windows VM successfully runs `auto_troubleshoot.py` with a PASS result.
- [ ] CompTIA 6-step documentation is complete.
- [ ] Remove static IPs and switch VirtualBox networking back to NAT (if desired for future labs).
- [ ] Delete the Python-generated firewall rules to reset the environment.

---

# Portfolio Artifacts

### Screenshot Checklist for GitHub
Capture these to include in your repository's image folder:
1. Wireshark GUI showing successful ICMP but missing TCP SYN (The broken state).
2. Wireshark GUI showing a successful 3-way TCP handshake (The fixed state).
3. The output of your `auto_troubleshoot.py` script showing a PASS.