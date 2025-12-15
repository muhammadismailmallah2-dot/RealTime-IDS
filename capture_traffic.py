#!/usr/bin/env python3
"""
capture_traffic.py
Simple pcap capture using scapy. Run as root (sudo) to sniff interfaces.
"""

from scapy.all import sniff, wrpcap
import argparse
import os
import time

def capture_packets(filename, count=2000, iface=None, timeout=None):
    print(f"[+] Capturing packets... Output file: {filename}")
    if iface:
        print(f"[+] Interface: {iface}")
    try:
        packets = sniff(count=count if count>0 else 0, iface=iface, timeout=timeout)
        # ensure resources dir exists
        os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
        wrpcap(filename, packets)
        print(f"[+] Capture completed: {filename} ({len(packets)} packets)")
    except PermissionError:
        print("[!] Permission denied: try running with sudo")
    except Exception as e:
        print(f"[!] Error while capturing: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture network traffic to a pcap file.")
    parser.add_argument("filename", help="output pcap file (e.g., normal.pcap)")
    parser.add_argument("--count", type=int, default=2000, help="number of packets to capture (0 for unlimited until timeout)")
    parser.add_argument("--iface", type=str, default=None, help="network interface to capture from (e.g., eth0)")
    parser.add_argument("--timeout", type=int, default=None, help="timeout in seconds (useful instead of count)")
    args = parser.parse_args()
    capture_packets(args.filename, args.count, args.iface, args.timeout)
