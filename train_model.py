#!/usr/bin/env python3
"""
train_model.py
Train a RandomForest classifier on dataset.csv
Produces IDS_Model.pkl, scaler.pkl, label_encoder.pkl, protocol_encoder.pkl
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

print("[+] Loading dataset...")
if not os.path.exists("dataset.csv"):
    print("[!] dataset.csv missing. Run combine_dataset.py first.")
    exit(1)

df = pd.read_csv("dataset.csv")
# Drop text fields we don't use for the numeric model
df = df.drop(columns=["src", "dst", "info"], errors="ignore")

# Fill/clean missing values
df = df.fillna(0)

# Encode protocol (some protocol strings)
le_protocol = LabelEncoder()
df["protocol"] = le_protocol.fit_transform(df["protocol"].astype(str))

# Encode labels (attack names)
le_label = LabelEncoder()
df["label_encoded"] = le_label.fit_transform(df["label"].astype(str))

# Choose features — keep 'time' optionally, but it's okay to include
X = df.drop(columns=["label", "label_encoded"], errors="ignore")
y = df["label_encoded"]

# Standard scale numeric features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.25, random_state=42
)

# Train RandomForest
print("[+] Training RandomForest...")
model = RandomForestClassifier(n_estimators=150, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save models and encoders
joblib.dump(model, "IDS_Model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(le_label, "label_encoder.pkl")
joblib.dump(le_protocol, "protocol_encoder.pkl")

print("\n[+] Training complete. Models saved: IDS_Model.pkl, scaler.pkl, label_encoder.pkl, protocol_encoder.pkl")
