import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, timezone
import os

os.makedirs('data', exist_ok=True)

def fetch_data():
    # 1. Fetch 14 days of historical currency data
    ticker = yf.Ticker("EURUSD=X")
    hist = ticker.history(period="14d")
    
    new_rows = []
    for date, row in hist.iterrows():
        # Format date to UTC string
        date_str = date.strftime("%Y-%m-%d %H:%M")
        
        # Structure the data as requested
        data_row = {
            "Date": date_str,
            "EUR_USD": round(row['Close'], 4),
            "USD_EUR": round(1 / row['Close'], 4),
            "Germany_Inflation_Rate": 2.2,  # Static for now
            "US_Inflation_Rate": 3.4,
            "Germany_GDP_Growth": 0.2,
            "US_GDP_Growth": 2.5
        }
        new_rows.append(data_row)
    
    df = pd.DataFrame(new_rows)
    
    # 2. Overwrite/Update the CSV
    file_path = 'data/economy_data.csv'
    # We use to_csv without 'append' here to ensure the 14-day window is clean
    df.to_csv(file_path, index=False)
    
    print(f"Successfully backfilled 14 days of data ending at {new_rows[-1]['Date']} UTC")

if __name__ == "__main__":
    fetch_data()