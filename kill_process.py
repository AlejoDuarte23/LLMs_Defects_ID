

import os
import subprocess
import sys

# Specify the port you're having trouble with


def find_process_using_port(port):
    """Find the process ID using the specified port."""
    command = f'netstat -aon | findstr :{port}'
    results = subprocess.run(command, capture_output=True, text=True, shell=True)
    lines = results.stdout.splitlines()
    for line in lines:
        if "LISTENING" in line:
            parts = line.split()
            return parts[-1]  # Return the PID
    return None

def kill_process(pid):
    """Kill the process with the specified PID."""
    command = f'taskkill /PID {pid} /F'
    print(command)
    subprocess.run(command, shell=True)
    print(f"Process {pid} has been killed.")

def kill_process(PORT = 11434):
    pid = find_process_using_port(PORT)
    kill_process(pid)

PORT = 11434
pid = find_process_using_port(PORT)
f'taskkill /PID {pid} /F'