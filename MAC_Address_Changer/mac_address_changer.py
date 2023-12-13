#!/usr/bin/env python

import subprocess
import argparse
import re
import sys


def grab_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to change your MAC address")
    parser.add_argument("-m", "--mac-address", dest="new_mac_address", help="You can add the desired new Mac Address")
    options = parser.parse_args()
    if not options.interface:
        parser.error("[+] Please specify the interface after --interface")
    elif not options.new_mac_address:
        parser.error("[+] Please specify the new mac address after --mac-address")
    return options


def change_mac(interface, new_mac_address):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac_address])
    subprocess.call(["ifconfig", interface, "up"])


def grab_current_mac(interface):
    try:
        ifconfig_result = subprocess.check_output(["ifconfig", interface])
        new_mac_address_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode('utf-8'))
        if new_mac_address_result:
            return new_mac_address_result.group(0)
        else:
            return None
    except subprocess.CalledProcessError:
        print("[-] Error fetching MAC address. Check if the specified interface is valid.")
        return None


options = grab_argument()
current_mac = grab_current_mac(options.interface)

if current_mac is None:
    print("[-] Your Network Adapter Does Not Have a MAC Address")
    sys.exit(1)  # Exit the script with an error code

print(f"[+] Your current MAC address: {current_mac}")

change_mac(options.interface, options.new_mac_address)
print(f"[+] Changing Your MAC address to {options.new_mac_address}")

current_mac = grab_current_mac(options.interface)

if options.new_mac_address == current_mac:
    print(f"[+] Your MAC address has been changed to: {current_mac}")
else:
    print("[-] Your MAC address has not been changed")
