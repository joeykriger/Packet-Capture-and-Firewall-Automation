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
    result = subprocess.run(tshark_cmd, capture_output = True, text = True, check = True)
    print("\n--- Protocol Hierarchy Statistics ---")
    print(result.stdout)
except FileNotFoundError:
    print("Error: tshark not found.")
except subprocess.CalledProcessError:
    print(f"Error reading file. Ensure '{capture_file}' exists in the directory.")
