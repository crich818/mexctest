import numpy as np
import pandas as pd
from datetime import datetime
import requests
import matplotlib.pyplot as plt

api_key = 'e369de76b2549dd0086f34191cfc3210'


# Function to fetch interest rate data from FRED
def fetch_interest_rate_data(api_key, start_date, end_date):
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id=DFF&api_key={api_key}&file_type=json&observation_start={start_date}&observation_end={end_date}"
    response = requests.get(url)
    data = response.json()
    observations = data['observations']
    
    # Create a DataFrame
    dates = [obs['date'] for obs in observations]
    rates = [float(obs['value']) for obs in observations]
    df = pd.DataFrame({'Date': dates, 'InterestRate': rates})
    
    # Convert date to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    return df

# Fetch interest rate data from 2000-01-01 to today
start_date = '2000-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')
interest_rate_data = fetch_interest_rate_data(api_key, start_date, end_date)
interest_rate_data['100movingaverage'] = interest_rate_data['InterestRate'].rolling(window=500).mean()
interest_rate_data = interest_rate_data.dropna(subset=['100movingaverage'])
print(interest_rate_data)

plt.plot(interest_rate_data['Date'], interest_rate_data['InterestRate'] , color="blue")
plt.plot(interest_rate_data['Date'], interest_rate_data['100movingaverage'] , color="red")
plt.show()