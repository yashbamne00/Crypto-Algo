# -*- coding: utf-8 -*-
"""Untitled10.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11qZgzggBJiBi7J0nHkuLcpkTZz5PufsQ
"""

import requests
import matplotlib.pyplot as plt
import time
from datetime import datetime

# Fetch data
p = {'resolution': "30m", 'symbol': "NOTUSD", 'start': int(time.time()) - 5077600, 'end': int(time.time())}
data = requests.get("https://cdn.india.deltaex.org/v2/history/candles", params=p).json()["result"]

# Extract time, close, high, and low prices
t, c, h, l = [], [], [], []
for d in reversed(data):  # Reverse to keep order correct
    t.append(datetime.utcfromtimestamp(d['time']))
    c.append(d['close'])
    h.append(d['high'])
    l.append(d['low'])

# Calculation
length, pos, entry, trades, signals = 250, None, 0, [], []
for i in range(length, len(c)):
    past_highs, past_lows = h[i-length:i], l[i-length:i]  # Store past values
    past_highs.sort()  # Sort highs to get highest
    past_lows.sort()  # Sort lows to get lowest
    HH, LL = past_highs[-1], past_lows[0]  # Highest high & lowest low

    if c[i] > HH and pos != 'long':  # Buy condition
        if pos == 'short': trades.append((entry - c[i]) * 100)
        pos, entry = 'long', c[i]
        signals.append((t[i], 'Buy'))

    elif c[i] < LL and pos != 'short':  # Sell condition
        if pos == 'long': trades.append((c[i] - entry) * 100)
        pos, entry = 'short', c[i]
        signals.append((t[i], 'Sell'))

# Output
print("\nFinal P&L:", round(sum(trades) * 500 * 85, 2))
print("Latest Signal:", 'buy' if signals and signals[-1][1] == 'Buy' else 'sell' if signals and signals[-1][1] == 'Sell' else 'hold')

# Plot
plt.figure(figsize=(6, 3))
plt.plot(t, c, label='Close Price', color='blue')
for time, s in signals:
    plt.axvline(x=time, color='green' if s == 'Buy' else 'red', linestyle='-', linewidth=1, alpha=0.5)
plt.legend()
plt.xticks(rotation=45)
plt.show()