import subprocess

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
    subprocess.run(tshark_cmd, check = True)
    print(f"Capture complete. Saved to {output_file}")
except FileNotFoundError:
    print("Error: tshark not found. Ensure Wireshark is installed and added to your PATH.")
except subprocess.CallProcessError:
    print("Error: Capture failed. Are you running as Administrator? Is the interface index correct?")