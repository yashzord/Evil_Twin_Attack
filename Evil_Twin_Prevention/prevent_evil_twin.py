import subprocess
import time
import re

# List of trusted SSIDs
TRUSTED_SSIDS = ['FBI Surveillance Van']  # Dynamically add the trusted SSIDs

def get_connected_ssid():
    """Gets the currently connected SSID."""
    try:
        result = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'], shell=True)
        result = result.decode('utf-8')
        ssid_search = re.search(r"SSID\s+:\s+(.*)", result)
        if ssid_search:
            return ssid_search.group(1).strip()
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving connected network: {e}")
        return None

def disconnect():
    """Disconnects from any network."""
    try:
        subprocess.run(['netsh', 'wlan', 'disconnect'], check=True)
        print("Blocked / Disconnected from the network as a preventive measure.")
    except subprocess.CalledProcessError:
        print("Failed to disconnect from the network.")

def monitor_for_untrusted_networks():
    """Monitors and disconnects if connected to an untrusted network."""
    while True:
        current_ssid = get_connected_ssid()
        if current_ssid and current_ssid not in TRUSTED_SSIDS:
            print(f"Preventive measure activated: Potential Rogue Network on air '{current_ssid}'. Proceeding with Caution as Evil Twin attack might happen.")
            disconnect()
            print(f"Evil Twin attack successfully prevented.")
        else:
            print(f"Currently connected to a trusted network: {current_ssid}")
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    monitor_for_untrusted_networks()
