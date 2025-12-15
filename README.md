# 📘 README.md

## 🛡️ Real-Time Intrusion Detection System (IDS)

### 🚀 Project Overview

This project is a **Real-Time Intrusion Detection System (IDS)** built using **Python, Machine Learning, and live network traffic**.
It monitors network packets in real time, detects malicious activities, triggers alerts, and visualizes attacks on a **SOC-style dashboard**.

The goal of this project is to **simulate how real-world IDS/SOC systems work**, combining packet sniffing, ML-based detection, alerting mechanisms, and dashboards.

---

## 🎯 Key Features

* 🔍 **Live packet sniffing** using Scapy
* 🧠 **Machine Learning–based attack detection** (RandomForest)
* ⚡ **Real-time alerts** with:

  * Colored terminal warnings
  * Alarm sounds
  * Voice alerts
  * Desktop notifications
* 📊 **SOC-style Streamlit dashboard**
* 📝 Persistent attack logging
* 🎛️ Supports multiple attack types:

  * Normal traffic
  * Port scanning
  * SYN flood
  * ICMP flood

---

## 🧱 Project Architecture

```
Network Traffic
   ↓
Packet Capture (Scapy)
   ↓
Feature Extraction (PyShark / Tshark)
   ↓
Dataset Creation (CSV)
   ↓
ML Model Training
   ↓
Real-Time Prediction
   ↓
Alerts + Logs + Dashboard
```

---

## 📂 Project Structure

```
IDS-Project/
├── capture_traffic.py
├── extract_features.py
├── combine_dataset.py
├── train_model.py
├── realtime_ids.py
├── dashboard.py
├── requirements.txt
├── resources/
│   ├── alert.mp3
│   ├── logo.png
│   └── jarvis_voice.wav
└── logs/
    └── attacks.txt
```

---

## 🧠 Machine Learning Details

* **Model:** RandomForestClassifier
* **Features used:**

  * Packet timestamp
  * Protocol
  * Packet length
* **Preprocessing:**

  * Label encoding
  * Feature scaling
* **Output:** Attack classification in real time

---

## 🖥️ Dashboard (SOC View)

The Streamlit dashboard provides:

* Live attack logs
* Attack frequency charts
* Packet intensity visualization
* SOC-style UI for monitoring incidents

Run with:

```bash
streamlit run dashboard.py
```

---

## 🧪 Attack Simulation (Lab Only)

This project supports **safe, local testing only** using tools like:

* `nmap` (port scanning)
* `hping3` (SYN flood simulation)
* `ping -f` (ICMP flood)

⚠️ **Never use these tools on unauthorized networks.**

---

## 🛠️ Requirements

* Python 3.x
* Linux (Ubuntu / Kali recommended)
* Tshark
* Scapy
* Streamlit
* Machine Learning libraries

Install dependencies:

```bash
pip3 install -r requirements.txt
```

---

## 🔐 Ethical Disclaimer

This project is built **strictly for educational and research purposes**.
Only test on systems and networks you own or have explicit permission to test.

---

## 🌟 Future Improvements

* WebSocket-based real-time dashboard updates
* Slack / Email alerts
* Dockerized demo mode
* SIEM integration
* JSON-based structured logs

---

## 👨‍💻 Author

**Ismail**
📌 *First cybersecurity project*
