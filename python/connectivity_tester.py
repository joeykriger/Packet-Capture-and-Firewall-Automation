import subprocess

target_ip = "192.168.10.10"
print(f"Testing Layer 3 connectivity to {target_ip}...")

result = subprocess.run(['ping', '-n', '4', target_ip], capture_output = True, text = True)

print(result.stdout)
if result.returncode == 0:
    print("Ping successful! Layer 3 is up.")
else:
    print("Ping failed! Check Layer 3 connectivity.")