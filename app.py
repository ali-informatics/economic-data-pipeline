import streamlit as st
import pandas as pd

st.set_page_config(page_title="5-Decade Econ Tracker", layout="wide")

df = pd.read_csv('data/economy_data.csv')
df['Date'] = pd.to_datetime(df['Date'])

st.title("🌐 Global Economic History: 1970 - 2026")

category = st.radio("**Select Metric:**", ["Currency (14 Days)", "GDP (50 Years)", "Inflation (50 Years)"], horizontal=True)

if "Currency" in category:
    sub_df = df[df['Type'] == 'Forex'].sort_values('Date')
    st.metric("EUR/USD", f"${sub_df['EUR_USD'].iloc[-1]:.4f}")
    st.line_chart(sub_df.set_index('Date')[['EUR_USD', 'USD_EUR']])

else:
    metric_name = "GDP_Growth" if "GDP" in category else "Inflation"
    # Filter for Macro data and the specific metric
    macro_df = df[(df['Type'] == 'Macro') & (df['Metric'] == metric_name)]
    
    # Pivot so we have USA and DEU as columns for the chart
    chart_pivot = macro_df.pivot(index='Date', columns='Country', values='Value')
    
    st.subheader(f"Historical {category} Trends")
    st.line_chart(chart_pivot)

if st.checkbox("Show Raw Data", value=True):
    st.dataframe(df, hide_index=True)