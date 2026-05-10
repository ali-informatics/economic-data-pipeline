import wbgapi as wb
import yfinance as yf
import pandas as pd
from datetime import datetime, timezone
import os

os.makedirs('data', exist_ok=True)

def fetch_data():
    # --- 1. FOREX (14 Days) ---
    ticker = yf.Ticker("EURUSD=X")
    forex_hist = ticker.history(period="14d")
    
    # --- 2. MACRO (5 Decades: 1970 - 2024) ---
    # Indicators: NY.GDP.MKTP.KD.ZG (GDP Growth %), FP.CPI.TOTL.ZG (Inflation %)
    countries = ['USA', 'DEU']
    indicators = {'NY.GDP.MKTP.KD.ZG': 'GDP_Growth', 'FP.CPI.TOTL.ZG': 'Inflation'}
    
    # Fetch from World Bank
    macro_data = wb.data.DataFrame(indicators.keys(), countries, time=range(1970, 2025), numericTimeKeys=True)
    
    # Reshape the data for our CSV
    macro_rows = []
    for (country, indicator), row in macro_data.iterrows():
        for year, value in row.items():
            macro_rows.append({
                "Date": f"{year}-01-01 00:00",
                "Country": country,
                "Metric": indicators[indicator],
                "Value": round(value, 2) if value is not None else 0
            })
    
    # Create final DataFrames
    forex_df = pd.DataFrame([{
        "Date": d.strftime("%Y-%m-%d %H:%M"),
        "EUR_USD": round(r['Close'], 4),
        "USD_EUR": round(1/r['Close'], 4),
        "Type": "Forex"
    } for d, r in forex_hist.iterrows()])

    macro_df = pd.DataFrame(macro_rows)
    macro_df["Type"] = "Macro"

    # Merge and Save
    full_df = pd.concat([forex_df, macro_df], ignore_index=True)
    full_df.to_csv('data/economy_data.csv', index=False)
    print("5-Decade Economic Engine fueled and ready!")

if __name__ == "__main__":
    fetch_data()