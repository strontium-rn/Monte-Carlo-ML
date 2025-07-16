import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_stock_data(symbol, start_date, end_date, base_price, volatility):
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    days = len(date_range)
    
    # Generate random walk for prices
    price_changes = np.random.normal(0, volatility, days)
    cumulative_changes = np.cumsum(price_changes)
    close_prices = base_price * (1 + cumulative_changes)
    
    # Ensure prices stay positive and realistic for NEPSE
    close_prices = np.abs(close_prices)
    close_prices = np.clip(close_prices, base_price*0.1, base_price*10)
    
    # Generate OHLC data with logical relationships
    data = []
    for i in range(days):
        close = close_prices[i]
        open_price = close * (1 + np.random.normal(0, 0.02))
        high = max(open_price, close) * (1 + abs(np.random.normal(0, 0.015)))
        low = min(open_price, close) * (1 - abs(np.random.normal(0, 0.015)))
        adj_close = close * (1 + np.random.normal(0, 0.001))
        
        # Generate volume (in lots of 10 shares)
        volume = int(abs(np.random.normal(5000, 3000))) * 10
        
        data.append([
            date_range[i].strftime('%Y-%m-%d'),
            round(open_price, 2),
            round(high, 2),
            round(low, 2),
            round(close, 2),
            round(adj_close, 2),
            volume
        ])
    
    df = pd.DataFrame(data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
    return df

# Define 5 mock NEPSE companies with different characteristics
companies = [
    {'symbol': 'NABIL', 'base_price': 800, 'volatility': 0.008},  # Banking - stable
    {'symbol': 'NICL', 'base_price': 600, 'volatility': 0.012},   # Insurance - moderate
    {'symbol': 'AHPC', 'base_price': 300, 'volatility': 0.015},   # Hydropower - volatile
    {'symbol': 'NTC', 'base_price': 900, 'volatility': 0.006},    # Telecom - stable
    {'symbol': 'SHL', 'base_price': 400, 'volatility': 0.010}     # Manufacturing - moderate
]

# Generate data for last 15 years
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=15*365)).strftime('%Y-%m-%d')

# Generate and save CSV for each company
for company in companies:
    print(f"Generating data for {company['symbol']}...")
    df = generate_stock_data(
        symbol=company['symbol'],
        start_date=start_date,
        end_date=end_date,
        base_price=company['base_price'],
        volatility=company['volatility']
    )
    
    # Remove weekends (NEPSE trading days)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[df['Date'].dt.dayofweek < 5]  # 0-4 = Monday-Friday
    
    filename = f"{company['symbol']}_historical_data.csv"
    df.to_csv(filename, index=False)
    print(f"Saved {filename} with {len(df)} trading days")

print("All 5 CSV files generated successfully!")