import pandas as pd
import os

# List of CSV files
files = [
    "resources/normal.csv",
    "resources/port_scan.csv",
    "resources/syn_flood.csv",
    "resources/icmp_flood.csv"
]


dfs = []

for f in files:
    if not os.path.exists(f):
        print(f"[!] Warning: {f} not found, skipping")
        continue

    if os.path.getsize(f) == 0:  # Check if file is truly empty
        print(f"[!] Warning: {f} is empty, skipping")
        continue

    print(f"[+] Reading file: {f}")
    try:
        df = pd.read_csv(f)
        dfs.append(df)
    except pd.errors.EmptyDataError:
        print(f"[!] Warning: {f} has no valid columns, skipping")

# Combine valid CSVs
if not dfs:
    print("[!] No valid CSV files found. Generate CSVs with extract_features.py first.")
else:
    combined = pd.concat(dfs, ignore_index=True)
    combined.to_csv("dataset.csv", index=False)
    print("[+] Combined dataset saved as dataset.csv")
    print("[+] Total rows:", len(combined))

