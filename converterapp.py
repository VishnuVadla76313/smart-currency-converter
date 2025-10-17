import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime, date, timedelta

# 👉 Replace with your actual API key from exchangerate-api.com
# Put your API key as a string in quotes
API_KEY = "742cfaf4804b5506d60b66dc"   # replace with your actual key
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}"
HISTORY_FILE = "conversion_history.csv"

st.set_page_config(page_title="Currency Converter", layout="centered")
st.title("💱 Currency Converter")

# --- User Inputs ---
col1, col2 = st.columns(2)
with col1:
    from_curr = st.text_input("From Currency (e.g., USD)", value="USD").upper().strip()
    amount = st.number_input("Amount", min_value=0.0, value=1.0, format="%.2f")
with col2:
    to_curr = st.text_input("To Currency (e.g., INR)", value="INR").upper().strip()
    precision = st.slider("Decimal Places", min_value=0, max_value=6, value=2)

# --- Conversion Function ---
def convert_currency(amount, from_curr, to_curr):
    try:
        url = f"{BASE_URL}/latest/{from_curr}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if data.get("result") != "success":
            return None

        rates = data.get("conversion_rates", {})
        if to_curr not in rates:
            return None

        rate = rates[to_curr]
        return float(amount) * float(rate)
    except Exception as e:
        st.error(f"API error: {e}")
        return None

# --- Convert Button ---
if st.button("Convert"):
    result = convert_currency(amount, from_curr, to_curr)
    if result is not None:
        formatted = round(result, precision)
        st.success(f"{amount} {from_curr} = {formatted} {to_curr}")

        # Save to history
        row = {
            "timestamp": datetime.utcnow().isoformat(),
            "from": from_curr,
            "to": to_curr,
            "amount": amount,
            "result": formatted
        }
        df = pd.DataFrame([row])
        if os.path.exists(HISTORY_FILE):
            df.to_csv(HISTORY_FILE, mode='a', header=False, index=False)
        else:
            df.to_csv(HISTORY_FILE, index=False)
    else:
        st.error("Conversion failed. Check your API key or currency codes.")

# --- Show History ---
if os.path.exists(HISTORY_FILE):
    if st.checkbox("Show Conversion History"):
        hist_df = pd.read_csv(HISTORY_FILE)
        st.dataframe(hist_df.tail(10))
        csv = hist_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download History CSV", data=csv, file_name=HISTORY_FILE)