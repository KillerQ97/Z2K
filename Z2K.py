import socket
import time
import os
from datetime import datetime

# =========================================================
# PROGRAM: KillerQ's Z2K (Zone 2 Killer)
# VERSION: 1.1.2
# =========================================================

# --- CONFIGURATION ---
DENON_IP = "192.168.68.63" 
CHECK_INTERVAL = 1          
LOG_FILE = "z2k_event_log.txt"

# --- STATE ---
block_count = 0

def log_event(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"[{timestamp}] {message}"
    try:
        with open(LOG_FILE, "a") as f:
            f.write(entry + "\n")
    except Exception:
        pass

def send_command(cmd):
    try:
        with socket.create_connection((DENON_IP, 23), timeout=2) as s:
            s.sendall((cmd + "\r").encode('ascii'))
            time.sleep(0.1) 
            data = s.recv(1024).decode('ascii', errors='ignore').strip()
            return data.replace('\r', ' ')
    except Exception:
        return "CONNECTION_ERROR"

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_status(raw_status):
    clear_console()
    print("=========================================")
    print("      KillerQ's Z2K - MONITOR ACTIVE     ")
    print(f"      SNEAKS KILLED: [ {block_count} ]")
    print("=========================================")
    print(f" AVR STATUS: {raw_status[:50]}")
    print("=========================================")
    print(" Status: Patrol in progress...")
    print(" Press Ctrl+C to stop monitoring.")

def run_guard():
    global block_count
    
    test = send_command("PW?")
    if "CONNECTION_ERROR" in test:
        print(f"ERROR: Could not connect to AVR at {DENON_IP}")
        return

    while True:
        status = send_command("Z2?")
        
        # Check if Zone 2 is ON
        if "Z2ON" in status:
            block_count += 1
            
            # 1. Execute Kill Sequence immediately
            send_command("Z2OFF")
            send_command("Z2STANDBY")
            time.sleep(0.5)
            send_command("SIMPLAY")
            
            # 2. Refresh the dashboard with the NEW block count
            display_status(status) 
            
            # 3. Print the Hunt Message AFTER the refresh so it stays visible
            print("\n [!!!] ROGUE EVENT DETECTED! INTERCEPTING... [!!!]")
            print(f" [OK] ZONE 2 KILLED. SNEAKS BLOCKED: {block_count}")
            print(" (Hope you enjoyed that hunt! This message will clear in 5 seconds)")
            
            log_event(f"KILLED ROGUE Z2 POWER (Event #{block_count})")
            
            # 4. Lock the screen for 5 seconds
            time.sleep(5) 
        else:
            # Normal patrol view
            display_status(status)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        run_guard()
    except KeyboardInterrupt:
        print(f"\nZ2K Stopped. Total sneaks killed: {block_count}")
