#!/usr/bin/env python3
"""
dashboard.py
Streamlit dashboard for the IDS (real-time visualization)
Run: streamlit run dashboard.py
"""

import streamlit as st
import time
import pandas as pd
import joblib
import os

st.set_page_config(page_title="IDS Dashboard", page_icon="🛡️", layout="wide")
st.markdown("""
<style>
body {
    background-color: #0b0f12;
    color: #cfeee7;
}
section.main > div {
    background-color: #071014;
}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Real-Time Intrusion Detection System")
st.markdown("### Built by **Ismail**")
if os.path.exists("resources/logo.png"):
    st.sidebar.image("resources/logo.png", width=150)

# load attack log (shared by realtime_ids.py)
LOG_FILE = "logs/attacks.txt"
attack_log = []

def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            lines = f.read().strip().splitlines()
        rows = []
        for line in lines:
            try:
                # Expect: "Mon Dec  1 12:00:00 2025 - label - length:123"
                parts = line.split(" - ")
                ts = parts[0]
                label = parts[1]
                length = int(parts[2].split(":")[1]) if len(parts)>2 else 0
                rows.append({"time": ts, "attack": label, "length": length})
            except Exception:
                continue
        return pd.DataFrame(rows)
    else:
        return pd.DataFrame(columns=["time", "attack", "length"])

st.sidebar.markdown("## Controls")
start_sidebar = st.sidebar.button("Start Local IDS (Console)")
st.sidebar.markdown("⚠️ Run the console IDS separately (sudo) for packet sniffing.")

st.subheader("Live Attack Log")
log_df = load_log()
log_placeholder = st.empty()
log_placeholder.table(log_df.tail(20))

st.subheader("Attack Stats")
if not log_df.empty:
    stats = log_df.groupby("attack").size().reset_index(name="count").sort_values("count", ascending=False)
    st.bar_chart(data=stats, x="attack", y="count")
    st.subheader("Attack intensity (packet length)")
    st.line_chart(log_df["length"].astype(float))
else:
    st.info("No attacks logged yet. Start the realtime IDS console or upload PCAPs and generate dataset.")

st.sidebar.markdown("## Tools & Tips")
st.sidebar.markdown("""
- Use `python3 capture_traffic.py sample.pcap --iface eth0 --timeout 60` to capture traffic.
- Use `python3 extract_features.py sample.pcap label` to create CSV.
- Use `python3 combine_dataset.py` then `python3 train_model.py`.
- Place models in project root.
""")

if st.button("Refresh Log"):
    log_placeholder.table(load_log().tail(20))

st.markdown("---")
st.markdown("Made with ❤️ by Ismail CyberTech — Demo SOC")
st.caption("RealTime-IDS • Live Monitoring • Ismail Cyber Defense")