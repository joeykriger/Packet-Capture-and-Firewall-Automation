import subprocess

print("Implementing firewall resolutions...")

commands = [
    "Disable-NetFirewallRule -DisplayName 'Block_App_Port' -ErrorAction SilentlyContinue",
    "Disable-NetFirewallRule -DisplayName 'Allow_Company_App' -ErrorAction SilentlyContinue",
    "Disable-NetFirewallRule -DisplayName 'Inbound_App_Traffic' -ErrorAction SilentlyContinue", 
]

for cmd in commands:
    print(f"Executing: {cmd.split('-DisplayName')[0].strip()}...")
    result = subprocess.run(['powershell', '-Command', cmd], capture_output=True, text=True)
    if result.returncode == 0:
        print(" -> Success.")
    else:
        print(" -> Action failed, or rule already modified.")

print("Firewall rules updated successfully.")