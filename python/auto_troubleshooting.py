import subprocess

target_ip = "192.168.10.10"
port = "8080"

print(f"--- Automated Troubleshooting Report for {target_ip} ---")

print("1. Testing Layer 3 (ICMP)...")
ping_result = subprocess.run(['ping', '-n', '1', target_ip], capture_output=True, text=True)

if ping_result.returncode == 0:
    print("   [PASS] Layer 3 connectivity established.")
else:
    print("   [FAIL] Layer 3 connectivity failed.")

print (f"2. Testing Layer 4 (TCP Port {port})...")
ps_cmd = f"Test-NetConnection -ComputerName {target_ip} -Port {port} -InformationLevel Quiet"
tcp_result = subprocess.run(['powershell', '-Command', ps_cmd], capture_output=True, text=True)

if "True" in tcp_result.stdout:
    print(f"   [PASS] Layer 4 connectivity established on port {port}.")
else:
    print(f"   [FAIL] Layer 4 connectivity failed.")

print("--- Report Complete ---")