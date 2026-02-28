import socket
import time
import os
from datetime import datetime

# =========================================================
# PROGRAM: KillerQ's Z2K (Zone 2 Killer)
# VERSION: 1.1
# DESCRIPTION: A network sentinel that intercepts rogue 
# Zone 2 power events on Denon/Marantz receivers.
# =========================================================

# --- CONFIGURATION ---
DENON_IP = "192.168.68.63"  # Replace with your AVR's Static IP
CHECK_INTERVAL = 2             # How often to check (seconds)
LOG_FILE = "z2k_event_log.txt"

# --- STATE ---
block_count = 0

def log_event(message):
    """Logs activity with timestamps for the 'Black Box' record."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"[{timestamp}] {message}"
    try:
        with open(LOG_FILE, "a") as f:
            f.write(entry + "\n")
    except Exception:
        pass

def send_command(cmd):
    """
    Sends Telnet commands via Port 23.
    Note for Pi/Linux/Arduino: This is a standard TCP socket 
    connection using ASCII encoding and Carriage Return (CR).
    """
    try:
        # Standard socket connection (works on Windows, Linux, and MacOS)
        with socket.create_connection((DENON_IP, 23), timeout=2) as s:
            s.sendall((cmd + "\r").encode('ascii'))
            time.sleep(0.1) # Small delay for AVR processing
            data = s.recv(1024).decode('ascii', errors='ignore').strip()
            return data.replace('\r', ' ')
    except Exception:
        return "CONNECTION_ERROR"

def clear_console():
    """Clears terminal screen for a clean 'Dashboard' view."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_status(raw_status):
    """The live monitoring dashboard."""
    clear_console()
    print("=========================================")
    print("      KillerQ's Z2K - MONITOR ACTIVE     ")
    print(f"      SNEAKS KILLED: [ {block_count} ]")
    print("=========================================")
    print(f" AVR STATUS: {raw_status[:50]}")
    print("=========================================")
    print(" Status: Patrol in progress...")
    print(" Press Ctrl+C to stop monitoring.")
    print(" (Running on Linux? Use crontab for boot)")

def run_guard():
    global block_count
    
    # Initial connection test
    test = send_command("PW?")
    if "CONNECTION_ERROR" in test:
        print(f"ERROR: Could not connect to AVR at {DENON_IP}")
        print("1. Check your IP address.")
        print("2. Ensure 'Network Control' is set to 'Always On' in AVR.")
        print("3. Ensure your device is on the same network.")
        return

    while True:
        # Check Zone 2 Status
        status = send_command("Z2?")
        display_status(status)

        # Logic: If Zone 2 reports ON (and isn't already OFF)
        if "Z2ON" in status and "Z2OFF" not in status:
            block_count += 1
            
            # --- Visual Alert for Windows Dashboard ---
            print("\n [!!!] ROGUE EVENT DETECTED! INTERCEPTING... [!!!]")
            log_event(f"KILLED ROGUE Z2 POWER (Event #{block_count})")
            
            # The 'Kill' Sequence
            send_command("Z2OFF")     # Standard Off
            send_command("Z2STANDBY") # Force Standby
            time.sleep(0.5)
            send_command("SIMPLAY")   # Force focus back to Main Zone
            
            # Victory Message
            print(f" [OK] ZONE 2 KILLED. SNEAKS BLOCKED: {block_count}")
            print(" (Hope you enjoyed that hunt! This message will clear in 5 seconds)")
            
            log_event("Restored Main Zone stability.")
            
            # Hold the message on screen for 5 seconds
            time.sleep(5) 
            
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    # Windows/Linux/Mac execution entry point
    try:
        run_guard()
    except KeyboardInterrupt:
        print(f"\nZ2K Stopped. Total sneaks killed: {block_count}")
