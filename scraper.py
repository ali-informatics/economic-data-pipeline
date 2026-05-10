import requests
import pandas as pd
from datetime import datetime
import os

# Create the data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

def fetch_data():
    # 1. Fetch Exchange Rates (Base: EUR)
    # Using a public API for simplicity
    url = "https://open.er-api.com/v6/latest/EUR"
    response = requests.get(url).json()
    
    rates = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "EUR_USD": response['rates'].get('USD'),
        "EUR_GBP": response['rates'].get('GBP'),
        "EUR_JPY": response['rates'].get('JPY'),
        "USD_EUR": 1 / response['rates'].get('USD')
    }

    # 2. Add placeholders for Economic Indicators (GDP/Inflation)
    # In a real scenario, you'd use a FRED API key here
    rates["US_Inflation_Rate"] = "3.4%"  # Example data point
    rates["Germany_GDP_Growth"] = "0.2%" 
    
    df = pd.DataFrame([rates])
    
    # 3. Save to CSV (Append mode)
    file_path = 'data/economy_data.csv'
    if not os.path.isfile(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)
    
    print(f"Successfully updated data at {rates['Date']}")

if __name__ == "__main__":
    fetch_data()