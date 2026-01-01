import streamlit as st
import pandas as pd
import requests

st.title("Crop Price Prediction")

# Load CSV locally to populate dropdowns if available
try:
    df = pd.read_csv("crop.csv")
    amc_options = sorted(df['Amc_Name'].dropna().unique())
    crop_options = sorted(df['Crop'].dropna().unique())
except Exception:
    df = None
    amc_options = []
    crop_options = []

amc = st.selectbox("Amc_Name", options=amc_options if amc_options else ["Enter value"])
crop = st.selectbox("Crop", options=crop_options if crop_options else ["Enter value"])

# Use a date picker and extract month/day for the model
date = st.date_input("Date")
month = date.month
day = date.day

if st.button("Predict"):
    payload = {"Amc_Name": amc, "Crop": crop, "Month": int(month), "Day": int(day)}

    try:
        resp = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            st.success(f"Minimum: {data.get('Minimum'):.2f} | Maximum: {data.get('Maximum'):.2f}")
        else:
            st.error(f"API error: {resp.status_code} - {resp.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to backend: {e}")
