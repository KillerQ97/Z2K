# KillerQ's Z2K (Zone 2 Killer)

### A Network Firewall for Denon & Marantz Receiver "CEC Ghosts" that often prevent your desired video input mode from switching properly

## The Problem

If you own an Nvidia Shield Pro (or similar HDMI-CEC components) and a Denon/Marantz AVR, you have likely encountered the "Zone 2 Bug." During HDMI-CEC handshakes, the Shield mistakenly sends a "Zone 2 Power On" command.

**This results in:**

* The AVR switching inputs randomly (often to a "Playback" or "Blu-ray" state).
* Your main screen going black while the AVR tries to process the rogue Zone 2 request.
* Secondary speakers (patio/bedroom/office) staying on all night.

## The Solution

Z2K is a lightweight Python sentinel script. It sits on your network and polls your receiver's API every 2 seconds. If it detects a rogue Zone 2 power-on event, it intercepts and kills the command in under 2 seconds, forcing the receiver back to Main Zone stability.

---

## Prerequisites

* **Network-Capable AVR:** Your Denon or Marantz receiver must have an Ethernet port or Wi-Fi.
* **Same Local Network:** The device running this script (PC, Raspberry Pi, etc.) must be on the same network/subnet as the AVR.
* **Static IP:** Your AVR should be set to a Static IP so the script does not lose the connection.

---

## Setup Instructions

### 1. Configure your AVR

* **Static IP:** In your AVR menu, go to Network > Settings and set DHCP to OFF. Note your IP (e.g., 192.168.xxx.xxx).
* **Network Control:** Set to "Always On". This allows the script to communicate with the receiver even when it is in standby.

### 2. Install Python

* Download Python 3 from python.org.

### 3. Run the Script

* **Windowed Mode (Watch the Chaos):** Run `python Z2K.py`. This opens a command window with a live dashboard and a "SNEAKS KILLED" counter. You can watch in real-time as the script intercepts rogue events.
* **Stealth Mode (Always Running):** Rename the file to `Z2K.pyw`. Double-clicking this will run the script invisibly in the background.
* **Auto-Start with Windows:** Press `Win + R`, type `shell:startup`, and place a shortcut to your `Z2K.pyw` file in that folder.
* **Check History:** Even in Stealth Mode, the script maintains a "black box" recorder. Open `z2k_event_log.txt` in the script folder to see a timestamped history of every blocked event.

---

## How to Test

Once the script is running, you can verify it is working by manually triggering a "Ghost" event:

1. Open the Z2K dashboard (Windowed Mode).
2. Grab your physical Denon/Marantz remote or use the mobile app.
3. Manually turn on **Zone 2**.
4. **The Result:** You should see the Zone 2 light on your receiver flash on and then immediately click back off within 2 seconds. The "SNEAKS KILLED" counter in the script window will tick up by one.

---

## FAQ & Troubleshooting

**Q: Does this work with Marantz?**
**A:** Yes. Marantz and Denon share the same IP control protocol.

**Q: My script says "CONNECTION_ERROR".**
**A:** Ensure your PC is not on a Guest Wi-Fi network and that your Windows Firewall is not blocking Python from accessing the local network. Also, verify that Network Control is Always On in the AVR menu.

**Q: Will this stop me from using Zone 2 on purpose?**
**A:** Yes. Since the script is a Guard, it will kill Zone 2 whenever it sees it. If you want to legitimately use your patio speakers, simply close the script (Ctrl+C) and restart it when you are finished.

---

## Compatibility Master List

I want to track which units this successfully fixes. If you have deployed Z2K, please join the Discussion on GitHub and post your setup:

* **Your AVR Model:** (e.g., Denon X1800H)
* **Your Input Device:** (e.g., Nvidia Shield Pro 2019)
* **Status:** Confirmed Working

---

*Created by KillerQ97*

---
