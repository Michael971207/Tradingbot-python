import numpy as np
import pandas as pd
import talib

# Load price data
df = pd.read_csv('price_data.csv')
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Calculate Bollinger Bands
df['MA20'] = df['close'].rolling(window=20).mean()
df['STD20'] = df['close'].rolling(window=20).std()
df['upper_band'] = df['MA20'] + 2 * df['STD20']
df['lower_band'] = df['MA20'] - 2 * df['STD20']

# Define entry rules
df['long_entry'] = np.where(df['close'] > df['upper_band'], 1, 0)
df['short_entry'] = np.where(df['close'] < df['lower_band'], -1, 0)
df['entry_signal'] = df['long_entry'] + df['short_entry']

# Define exit rules
df['exit_signal'] = np.where(df['entry_signal'].shift(1) != df['entry_signal'], -df['entry_signal'].shift(1), 0)

# Calculate PnL
df['pnl'] = df['close'] * df['entry_signal'].shift(1) + df['close'] * df['exit_signal'].shift(1)
df['cumulative_pnl'] = df['pnl'].cumsum()

# Plot the results
import matplotlib.pyplot as plt
plt.plot(df['cumulative_pnl'])
plt.show()
