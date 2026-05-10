import requests
import pandas as pd
from datetime import datetime, timezone
import os

os.makedirs('data', exist_ok=True)

def fetch_data():
    # 1. Fetch EUR Base Rates
    url = "https://open.er-api.com/v6/latest/EUR"
    response = requests.get(url).json()
    
    # Force UTC time formatting
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    
    # Exact requested columns
    data_row = {
        "Date": now_utc,
        "EUR_USD": response['rates'].get('USD'),
        "USD_EUR": 1 / response['rates'].get('USD'),
        "Germany_Inflation_Rate": 2.2,  # Numeric dummy data for charts
        "US_Inflation_Rate": 3.4,
        "Germany_GDP_Growth": 0.2,
        "US_GDP_Growth": 2.5
    }
    
    df = pd.DataFrame([data_row])
    
    file_path = 'data/economy_data.csv'
    if not os.path.isfile(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)
    
    print(f"Successfully updated data at {data_row['Date']} UTC")

if __name__ == "__main__":
    fetch_data()