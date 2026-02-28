# KillerQ's Z2K (Zone2 Killer)
### A Network Firewall for Denon & Marantz Receiver "CEC Ghosts" that often prevent your desired video input mode from switching properly

## The Problem
If you own an **Nvidia Shield Pro** (or other similar HDMI components) and a **Denon/Marantz AVR**, you’ve likely encountered the "Zone 2 Bug." During HDMI-CEC handshakes, the Shield mistakenly sends a "Zone 2 Power On" command. 

**This results in:**
* The AVR switching inputs randomly.
* The main screen going black while the AVR tries to process Zone 2.
* Secondary speakers (patio/bedroom) staying on all night.

## The Solution
**Z2K** is a lightweight Python script that acts as a dedicated monitor for your AVR. It polls your receiver's network API every 2 seconds. If it detects a "rogue" Zone 2 power-on event, it intercepts and kills the command in under 2 seconds, restoring focus to your Main Zone automatically.

---

## Setup Instructions

### 1. Configure your AVR
* **Static IP:** Set your AVR to a Static IP (e.g., `192.168.68.55`).
* **Network Control:** Set to **"Always On"** in the AVR settings.

### 2. Install Python
* Download **Python 3** from [python.org](https://www.python.org/).

### 3. Run the Script
* **Windows (Background):** Rename the script to `Z2K.pyw` and double-click to run invisibly.
* **Logs:** Check `z2k_event_log.txt` in the script folder for history.

---
*Created by KillerQ97*
