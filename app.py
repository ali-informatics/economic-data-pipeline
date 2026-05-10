import streamlit as st
import pandas as pd

st.set_page_config(page_title="Global Econ Tracker", layout="wide")

# 1. Load the Data
@st.cache_data(ttl=3600) # Refreshes cache every hour
def load_data():
    df = pd.read_csv('data/economy_data.csv')
    return df

df = load_data()

# 2. Header & Live Status
st.title("🌐 Global Economic Data Pipeline")
last_updated = df['Date'].iloc[-1]
st.write(f"**Status:** Live | **Last Updated:** `{last_updated}`")

# 3. Main Metrics
st.subheader("Current Exchange Rates (vs EUR)")
cols = st.columns(4)
cols[0].metric("EUR/USD", f"${df['EUR_USD'].iloc[-1]:.4f}")
cols[1].metric("EUR/GBP", f"£{df['EUR_GBP'].iloc[-1]:.4f}")
cols[2].metric("EUR/JPY", f"¥{df['EUR_JPY'].iloc[-1]:.2f}")
cols[3].metric("USD/EUR", f"€{df['USD_EUR'].iloc[-1]:.4f}")

# 4. Trends Chart
st.subheader("Historical Trends")
chart_data = df.set_index('Date')[['EUR_USD', 'EUR_GBP']]
st.line_chart(chart_data)

# 5. Raw Data Toggle
if st.checkbox("Show Raw Data"):
    st.dataframe(df)