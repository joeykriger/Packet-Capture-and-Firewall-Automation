import subprocess 

print("Auditing Windows Defender Firewall for rules affecting port 8080...")

# 1. Get the port filters matching 8080
# 2. Pipeline them to Get-NetFirewallRule to fetch the display names and actions
# 3. Create a custom PSCustomObject to combine both Rule and Port Filter properties for output
ps_cmd = (
    "Get-NetFirewallRule | ForEach-Object { "
    "  $rule = $_; "
    "  $pf = $rule | Get-NetFirewallPortFilter; "
    "  if ((($pf.LocalPort -join ',') -match '8080') -or (($pf.RemotePort -join ',') -match '8080')) { "
    "    [PSCustomObject]@{ "
    "      DisplayName = $rule.DisplayName; "
    "      Direction   = $rule.Direction; "
    "      Action      = $rule.Action; "
    "      Protocol    = $pf.Protocol; "
    "      LocalPort   = ($pf.LocalPort -join ','); "
    "      RemotePort  = ($pf.RemotePort -join ',') "
    "    } "
    "  } "
    "} | Format-Table -AutoSize"
)

result = subprocess.run(['powershell', '-NoProfile', '-Command', ps_cmd], capture_output=True, text=True)

print("\n--- Firewall Audit Results ---")
if result.stdout.strip():
    print(result.stdout)
else:
    # Provide stderr and exit code to diagnose PowerShell errors
    print("No rules found affecting port 8080.")
    if result.stderr.strip():
        print("\nPowerShell stderr:")
        print(result.stderr)
    print(f"\nPowerShell exit code: {result.returncode}")
