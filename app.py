import streamlit as st
import pandas as pd
import requests

st.title("Crop Price Prediction (Streamlit)")

try:
    df = pd.read_csv("crop.csv")
    amc_options = sorted(df['Amc_Name'].dropna().unique())
    crop_options = sorted(df['Crop'].dropna().unique())
except Exception:
    amc_options = []
    crop_options = []

if amc_options:
    amc = st.selectbox("Amc_Name", amc_options)
else:
    amc = st.text_input("Amc_Name")

if crop_options:
    crop = st.selectbox("Crop", crop_options)
else:
    crop = st.text_input("Crop")

month = st.slider("Month", 1, 12, 1)
day = st.slider("Day", 1, 31, 1)

if st.button("Predict"):
    payload = {"Amc_Name": amc, "Crop": crop, "Month": int(month), "Day": int(day)}
    try:
        resp = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=10)
        if resp.ok:
            data = resp.json()
            st.success(f"Minimum: {data.get('Minimum'):.2f} | Maximum: {data.get('Maximum'):.2f}")
        else:
            st.error(f"API error {resp.status_code}: {resp.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to reach backend: {e}")
