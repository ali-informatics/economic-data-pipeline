import streamlit as st
import pandas as pd

# Set page config for a professional look
st.set_page_config(page_title="Ali Informatics | Econ-Tracker", layout="wide")

st.title("📈 Global Economic Data Pipeline")
st.markdown("Automated historical analysis and currency tracking.")

# 1. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('data/economy_data.csv')
    # Ensure Date is actually a datetime object for better sorting
    df['Date'] = pd.to_datetime(df['Date'])
    return df

try:
    df = load_data()

    # 2. Sidebar Navigation
    st.sidebar.header("Dashboard Controls")
    selection = st.sidebar.radio("Select Data Stream:", ["Forex", "Macro"])

    # 3. Filtering Logic
    filtered_df = df[df['Type'] == selection].sort_values('Date', ascending=False)

    # 4. Display Content based on Selection
    if selection == "Forex":
        st.subheader("💱 EUR/USD Exchange Rate (Last 14 Days)")
        
        # Display the Graph
        st.line_chart(filtered_df, x='Date', y='EUR_USD')
        
        # Display CLEAN Table (Only Currency Columns)
        st.write("### Raw Exchange Data")
        st.dataframe(filtered_df[['Date', 'EUR_USD', 'USD_EUR']], use_container_width=True)

    else:
        st.subheader("🌎 Macroeconomic Indicators (5 Decades)")
        
        # Sub-filter for Macro (so the graph doesn't look like a mess)
        metric = st.selectbox("Choose Metric:", filtered_df['Metric'].unique())
        country = st.selectbox("Choose Country:", filtered_df['Country'].unique())
        
        plot_df = filtered_df[(filtered_df['Metric'] == metric) & (filtered_df['Country'] == country)]
        
        # Display the Graph
        st.line_chart(plot_df, x='Date', y='Value')
        
        # Display CLEAN Table (Only Macro Columns)
        st.write(f"### Raw {metric} Data: {country}")
        st.dataframe(plot_df[['Date', 'Country', 'Metric', 'Value']], use_container_width=True)

except Exception as e:
    st.error(f"Waiting for data pipeline to complete... Error: {e}")
    st.info("If you just pushed the code, wait 1 minute for the GitHub Action to generate the CSV.")

st.sidebar.markdown("---")
st.sidebar.info("Data automatically updated via GitHub Actions.")