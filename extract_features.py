#!/usr/bin/env python3
"""
extract_features.py
Extract simple features from a pcap into CSV using pyshark (tshark required).
Usage: python extract_features.py file.pcap label
"""

import pyshark
import pandas as pd
import sys
import os

def extract_features(pcap_file, label):
    print(f"[+] Processing {pcap_file} ... (label={label})")
    cap = pyshark.FileCapture(pcap_file, only_summaries=True)
    data = []
    for pkt in cap:
        try:
            # some summaries have protocol, length, source, destination, info, time
            data.append({
                "time": float(pkt.time),
                "protocol": pkt.protocol,
                "length": int(pkt.length),
                "src": pkt.source,
                "dst": pkt.destination,
                "info": pkt.info,
                "label": label
            })
        except Exception:
            continue
    cap.close()
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_features.py file.pcap label")
        sys.exit(1)
    pcap_file = sys.argv[1]
    label = sys.argv[2]
    df = extract_features(pcap_file, label)
    output_csv = os.path.splitext(pcap_file)[0] + ".csv"
    df.to_csv(output_csv, index=False)
    print(f"[+] CSV saved: {output_csv} (rows={len(df)})")
