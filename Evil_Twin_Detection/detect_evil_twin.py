import pywifi
from pywifi import const
import time
from collections import defaultdict
import tkinter as tk
from tkinter import messagebox
import datetime

def get_wifi_interface():
    wifi = pywifi.PyWiFi()
    ifaces = wifi.interfaces()
    if len(ifaces) == 0:
        print("No Wi-Fi interface found.")
        return None
    iface = ifaces[0]
    return iface

def scan_networks(iface):
    iface.scan()
    time.sleep(3) 
    return iface.scan_results()

def establish_baseline(iface, target_ssid, scan_count=5):
    print(f"Establishing baseline for SSID: {target_ssid}")
    baseline_bssids = {}
    for i in range(scan_count):
        networks = scan_networks(iface)
        for network in networks:
            ssid = network.ssid
            bssid = network.bssid.upper()
            if ssid == target_ssid:
                baseline_bssids[bssid] = {
                    'signal': network.signal,
                    'channel': network.freq
                }
        print(f"Scan {i+1}/{scan_count} completed.")
    
    if baseline_bssids:
        print(f"Baseline BSSIDs for '{target_ssid}': {list(baseline_bssids.keys())}")
    else:
        print(f"No networks found with SSID '{target_ssid}'.")
    return baseline_bssids

def detect_new_bssids(iface, target_ssid, baseline_bssids):
    networks = scan_networks(iface)
    current_bssids = {}
    for network in networks:
        ssid = network.ssid
        bssid = network.bssid.upper()
        if ssid == target_ssid:
            current_bssids[bssid] = {
                'signal': network.signal,
                'channel': network.freq,
                'timestamp': datetime.datetime.now()
            }
    new_bssids = {}
    for bssid, info in current_bssids.items():
        if bssid not in baseline_bssids:
            new_bssids[bssid] = info
    return new_bssids

def alert_user(ssid, new_bssids):
    root = tk.Tk()
    root.withdraw()
    bssid_info = ''
    log_entries = []
    for bssid, info in new_bssids.items():
        bssid_info += (
            f"BSSID: {bssid}\n"
            f"Signal Strength: {info['signal']} dBm\n"
            f"Channel: {info['channel']} MHz\n"
            f"Time Detected: {info['timestamp']}\n\n"
        )
        log_entries.append(
            f"{info['timestamp']}, BSSID: {bssid}, Signal: {info['signal']} dBm, "
            f"Channel: {info['channel']} MHz\n"
        )
    
    message = f"New BSSID detected for SSID: {ssid}\n\n{bssid_info}Evil Twin attack Detected."
    messagebox.showwarning("Evil Twin Alert", message)
    root.destroy()
    
    with open("bssid_log.txt", "a") as log:
        for entry in log_entries:
            log.write(entry)

def main():
    target_ssid = "FBI Surveillance Van"
    iface = get_wifi_interface()
    if iface is None:
        return

    baseline_bssids = establish_baseline(iface, target_ssid, scan_count=5)

    if not baseline_bssids:
        print(f"Cannot establish baseline without known BSSIDs for SSID '{target_ssid}'. Exiting.")
        return

    print("Starting continuous monitoring...")
    while True:
        new_bssids = detect_new_bssids(iface, target_ssid, baseline_bssids)
        if new_bssids:
            print(f"New BSSID(s) detected for SSID '{target_ssid}': {list(new_bssids.keys())}")
            alert_user(target_ssid, new_bssids)
        else:
            print(f"No new BSSIDs detected for SSID '{target_ssid}'.")
        time.sleep(5)

if __name__ == "__main__":
    main()
