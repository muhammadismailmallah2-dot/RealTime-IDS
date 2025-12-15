#!/usr/bin/env python3
"""
realtime_ids.py
Real-time IDS with:
- ASCII banner + animation
- colored console alerts
- plays sound on attack (fallbacks)
- desktop notifications (Linux notify-send)
- voice alerts (pyttsx3)
- persistent logs
Run with sudo to sniff network interfaces.
"""

import os
import time
import random
import subprocess
import joblib
import pandas as pd
from colorama import Fore, Style, init as colorama_init

# initialize colorama
colorama_init(autoreset=True)

# Load models/encoders
MODEL_FILE = "IDS_Model.pkl"
SCALER_FILE = "scaler.pkl"
LABEL_ENCODER_FILE = "label_encoder.pkl"
PROTOCOL_ENCODER_FILE = "protocol_encoder.pkl"

def safe_load(path):
    try:
        return joblib.load(path)
    except Exception as e:
        print(f"[!] Failed to load {path}: {e}")
        return None

model = safe_load(MODEL_FILE)
scaler = safe_load(SCALER_FILE)
label_encoder = safe_load(LABEL_ENCODER_FILE)
protocol_encoder = safe_load(PROTOCOL_ENCODER_FILE)

# resources
ALERT_SOUND = "resources/alert.mp3"
LOG_FILE = "logs/attacks.txt"

# optional pyttsx3 voice
try:
    import pyttsx3
    engine = pyttsx3.init()
    def speak(text):
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception:
            pass
except Exception:
    def speak(text):
        pass

# sound function with fallback
def play_sound(path=ALERT_SOUND):
    # try playsound first
    try:
        from playsound import playsound
        playsound(path, block=False)
        return
    except Exception:
        pass
    # fallback to system player (Linux)
    if os.name != "nt":
        for cmd in (["paplay", path], ["aplay", path], ["mpg123", path], ["ffplay", "-nodisp", "-autoexit", path]):
            try:
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
            except Exception:
                continue

# desktop notification on Linux (notify-send)
def notify(title, message):
    if os.name == "nt":
        # Windows notifications not implemented here (add if needed)
        return
    else:
        try:
            subprocess.Popen(["notify-send", title, message])
        except Exception:
            pass

# ascii banner
BANNER = r"""
██╗███████╗███╗   ███╗ █████╗ ██╗██╗     
██║██╔════╝████╗ ████║██╔══██╗██║██║     
██║███████╗██╔████╔██║███████║██║██║     
██║╚════██║██║╚██╔╝██║██╔══██║██║██║     
██║███████║██║ ╚═╝ ██║██║  ██║██║███████╗
╚═╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝


         ISMAIL CYBER DEFENSE SYSTEM
"""

def hacker_animation(iterations=40, width=80, delay=0.02):
    try:
        for _ in range(iterations):
            line = "".join(random.choice("01*#@$%<>") for _ in range(width))
            print(Fore.GREEN + line)
            time.sleep(delay)
            # clear last line sometimes for effect (optional)
    except KeyboardInterrupt:
        pass

# packet -> features
def packet_to_features(packet):
    """
    Accepts a scapy packet and returns label string.
    We expect the model to expect: time, protocol, length
    """
    try:
        protocol_field = getattr(packet, "proto", None)
        # some scapy layers have .proto as int; convert to str for encoder
        protocol_str = str(protocol_field if protocol_field is not None else packet.name if hasattr(packet,'name') else 0)
        # transform protocol with encoder — if fail, use 0
        try:
            protocol_encoded = protocol_encoder.transform([protocol_str])[0]
        except Exception:
            # fallback: try mapping numeric or use 0
            protocol_encoded = 0

        length = len(packet)
        timestamp = time.time()
        df = pd.DataFrame([{
            "time": timestamp,
            "protocol": protocol_encoded,
            "length": length
        }])
        scaled = scaler.transform(df)
        prediction = model.predict(scaled)
        label = label_encoder.inverse_transform(prediction)[0]
        return label, timestamp, length
    except Exception:
        return "unknown", time.time(), 0

# process packet callback
attack_log = []
packet_count = 0

def process_packet(packet):
    global packet_count
    packet_count += 1
    label, ts, length = packet_to_features(packet)

    if label.lower() != "normal" and label.lower() != "unknown":
        # colored console
        print(Fore.RED + Style.BRIGHT + f"\n🚨 ALERT: {label.upper()} DETECTED (len={length}) at {time.ctime(ts)}")
        # play sound
        play_sound()
        # voice
        speak(f"Warning. {label} attack detected.")
        # desktop notify
        notify("Intrusion Detected", f"{label} detected")
        # append to attack_log and persistent file
        entry = f"{time.ctime(ts)} - {label} - length:{length}\n"
        attack_log.append({"time": ts, "attack": label, "length": length})
        os.makedirs(os.path.dirname(LOG_FILE) or ".", exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(entry)
    else:
        # optionally show normal packets every X packets
        if packet_count % 100 == 0:
            print(Fore.GREEN + f"[{time.ctime()}] Normal traffic observed (total pkts: {packet_count})")

# start monitoring
def start_monitoring(iface=None):
    try:
        import scapy.all as scapy
    except Exception as e:
        print("[!] scapy not installed or failed:", e)
        return

    print(BANNER)
    time.sleep(0.7)
    hacker_animation(20, width=60, delay=0.03)
    print(Fore.CYAN + "\n🔥 Real-Time IDS Started  — Press CTRL+C to stop.\n")

    try:
        scapy.sniff(prn=process_packet, store=False, iface=iface)
    except PermissionError:
        print("[!] Permission denied. Try running with sudo.")
    except Exception as e:
        print(f"[!] Error while sniffing: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run real-time IDS")
    parser.add_argument("--iface", help="Interface to sniff (e.g., eth0)")
    args = parser.parse_args()
    start_monitoring(args.iface)
