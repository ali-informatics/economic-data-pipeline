import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Global Econ Tracker", layout="wide")

@st.cache_data(ttl=3600)
def load_data():
    # Load and ensure Date is treated as a datetime object
    try:
        df = pd.read_csv('data/economy_data.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except FileNotFoundError:
        return pd.DataFrame() # Returns empty if no data yet

df = load_data()

st.title("🌐 Global Economic Data Pipeline")

if df.empty:
    st.warning("Awaiting first data pipeline run. Please trigger the GitHub Action.")
else:
    # --- Time Filtering (Last 14 Days) ---
    fourteen_days_ago = datetime.utcnow() - timedelta(days=14)
    df_filtered = df[df['Date'] >= fourteen_days_ago].copy()
    
    # Create a Date-only column for the chart X-axis
    df_filtered['Date_Only'] = df_filtered['Date'].dt.strftime('%Y-%m-%d')
    
    # --- Header & Status ---
    last_updated = df_filtered['Date'].iloc[-1].strftime("%Y-%m-%d %H:%M")
    st.write(f"**Status:** Live | **Last Updated:** `{last_updated} UTC`")

    # --- Interactive Controls ---
    st.write("---")
    category = st.radio(
        "**Select Metric to Visualize:**", 
        ["Currency", "GDP", "Inflation"], 
        horizontal=True
    )

    # --- Dynamic Display Logic ---
    if category == "Currency":
        cols = st.columns(2)
        cols[0].metric("EUR/USD", f"${df_filtered['EUR_USD'].iloc[-1]:.4f}")
        cols[1].metric("USD/EUR", f"€{df_filtered['USD_EUR'].iloc[-1]:.4f}")
        
        st.subheader("Currency Trends (Last 14 Days)")
        chart_data = df_filtered.set_index('Date_Only')[['EUR_USD', 'USD_EUR']]
        st.line_chart(chart_data)

    elif category == "GDP":
        cols = st.columns(2)
        cols[0].metric("US GDP Growth", f"{df_filtered['US_GDP_Growth'].iloc[-1]}%")
        cols[1].metric("Germany GDP Growth", f"{df_filtered['Germany_GDP_Growth'].iloc[-1]}%")
        
        st.subheader("GDP Trends (Last 14 Days)")
        chart_data = df_filtered.set_index('Date_Only')[['US_GDP_Growth', 'Germany_GDP_Growth']]
        st.line_chart(chart_data)

    elif category == "Inflation":
        cols = st.columns(2)
        cols[0].metric("US Inflation Rate", f"{df_filtered['US_Inflation_Rate'].iloc[-1]}%")
        cols[1].metric("Germany Inflation Rate", f"{df_filtered['Germany_Inflation_Rate'].iloc[-1]}%")
        
        st.subheader("Inflation Trends (Last 14 Days)")
        chart_data = df_filtered.set_index('Date_Only')[['US_Inflation_Rate', 'Germany_Inflation_Rate']]
        st.line_chart(chart_data)

    st.write("---")

    # --- Raw Data Table ---
    if st.checkbox("Show Raw Data", value=True): # Default is ON
        # Enforce exact column order
        ordered_cols = [
            'Date', 'EUR_USD', 'USD_EUR', 
            'Germany_Inflation_Rate', 'US_Inflation_Rate', 
            'Germany_GDP_Growth', 'US_GDP_Growth'
        ]
        # Display the 14-day filtered data
        st.dataframe(df_filtered[ordered_cols], hide_index=True)