import socket
import time
from datetime import datetime
import os

# --- CONFIGURATION ---
DENON_IP = "192.168.XXX.XXX" # (ADD YOU OWN AVR IP HERE)
CHECK_INTERVAL = 2          
LOG_FILE = "shield_guard_log.txt"

# Tracking
stop_count = 0

def log_event(message):
    timestamp = datetime.now().strftime('%H:%M:%S')
    entry = f"[{timestamp}] {message}"
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")
    return entry

def send_cmd(cmd):
    try:
        with socket.create_connection((DENON_IP, 23), timeout=1) as s:
            s.sendall((cmd + "\r").encode('ascii'))
            time.sleep(0.1)
            data = s.recv(1024).decode('ascii', errors='ignore').strip()
            return data.replace('\r', ' ')
    except:
        return "RECONNECTING..."

def refresh_screen(status_text):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=========================================")
    print("   DENON SHIELD GUARD: V12 MONITOR       ")
    print(f"   BLOCK COUNTER: [ {stop_count} ]")
    print("=========================================")
    print(f" STATUS: {status_text[:50]}")
    print("=========================================")
    print(" (Watching for Shield CEC 'Zone 2' bugs...)")

try:
    while True:
        raw_status = send_cmd("Z2?")
        
        # Update the clean UI
        refresh_screen(raw_status)

        # Logic: If 'Z2ON' is in the mess, but 'Z2OFF' is not.
        if "Z2ON" in raw_status and "Z2OFF" not in raw_status:
            stop_count += 1
            log_event(f"INTERCEPTED SNEAK #{stop_count}")
            
            print("\n" + "!"*40)
            print(f" KILLING ZONE 2 (SNEAK #{stop_count})...")
            
            # The Kill Sequence
            send_cmd("Z2OFF")
            send_cmd("Z2STANDBY")
            time.sleep(0.5)
            send_cmd("SIMPLAY") 
            
            time.sleep(1.5) # Let it settle
            print(" SUCCESS: ZONE 2 NEUTRALIZED.")
            print("!"*40)
            time.sleep(1) # Show success message briefly before refresh
            
        time.sleep(CHECK_INTERVAL)

except KeyboardInterrupt:
    print(f"\n\nStopped. Total sneaks blocked: {stop_count}")
