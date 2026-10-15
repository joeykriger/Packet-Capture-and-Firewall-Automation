import subprocess

target_port = 8080
timeout_seconds = 60

print(f"Auditing Windows Defender Firewall for rules affecting port {target_port}...")

# 1. Get the port filters matching 8080
# 2. Add them to Get-NetFirewallRule to fetch the display names and actions
# 3. Create a custom PSCustomObject to combine both Rule and Port Filter properties for output
ps_cmd = f"""
$ErrorActionPreference = 'Stop'
$targetPort = {target_port}

function Test-PortMatch {{
    param([object[]]$PortValues, [int]$TargetPort)

    foreach ($value in $PortValues) {{
        foreach ($entry in ([string]$value -split ',')) {{
            $entry = $entry.Trim()
            if ($entry -eq [string]$TargetPort) {{
                return $true
            }}

            $range = [regex]::Match($entry, '^(\\d+)-(\\d+)$')
            if ($range.Success) {{
                $rangeStart = [int]$range.Groups[1].Value
                $rangeEnd = [int]$range.Groups[2].Value
                if ($TargetPort -ge $rangeStart -and $TargetPort -le $rangeEnd) {{
                    return $true
                }}
            }}
        }}
    }}

    return $false
}}

$portFilters = Get-NetFirewallPortFilter -PolicyStore ActiveStore
$results = foreach ($pf in $portFilters) {{
    if ((Test-PortMatch -PortValues $pf.LocalPort -TargetPort $targetPort) -or
        (Test-PortMatch -PortValues $pf.RemotePort -TargetPort $targetPort)) {{
        $rules = Get-NetFirewallRule -AssociatedNetFirewallPortFilter $pf -PolicyStore ActiveStore
        foreach ($rule in $rules) {{
            [PSCustomObject]@{{
                DisplayName = $rule.DisplayName
                Direction = $rule.Direction
                Action = $rule.Action
                Protocol = $pf.Protocol
                LocalPort = ($pf.LocalPort -join ',')
                RemotePort = ($pf.RemotePort -join ',')
            }}
        }}
    }}
}}

$results | Sort-Object DisplayName, Direction, Action, Protocol, LocalPort, RemotePort -Unique | Format-Table -AutoSize
"""

print("\n--- Firewall Audit Results ---")
try:
    result = subprocess.run(
        ['powershell', '-NoProfile', '-Command', ps_cmd],
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
    )
except subprocess.TimeoutExpired:
    print(f"Firewall audit timed out after {timeout_seconds} seconds.")
    raise SystemExit(1)
# Provide stderr and exit code to diagnose PowerShell errors
if result.returncode != 0:
    if result.stdout.strip():
        print(result.stdout)
    if result.stderr.strip():
        print("\nPowerShell stderr:")
        print(result.stderr)
    print(f"\nPowerShell exit code: {result.returncode}")
    raise SystemExit(result.returncode)

if result.stdout.strip():
    print(result.stdout)
else:
    print(f"No rules found affecting port {target_port}.")