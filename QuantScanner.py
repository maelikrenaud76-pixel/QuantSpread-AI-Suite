import yfinance as yf
import pandas as pd
import itertools

# ============================================================
# PAIRS TO SCAN
# ============================================================
TICKERS = ["MSFT","AAPL","GOOG","AMZN","META","TSLA",
           "NVDA","JPM","BAC","KO","PEP","ORCL"]

# ============================================================
# DOWNLOAD DATA
# ============================================================
print("Downloading prices...")
data = yf.download(TICKERS, start="2018-01-01")["Close"].dropna()

# ============================================================
# SCAN PAIRS
# ============================================================
pairs = []
for t1, t2 in itertools.combinations(TICKERS, 2):
    corr = data[t1].corr(data[t2])
    pairs.append((t1, t2, corr))

# Sort descending
pairs_sorted = sorted(pairs, key=lambda x: abs(x[2]), reverse=True)

print("\nTOP 10 BEST PAIRS:")
for p in pairs_sorted[:10]:
    print(f"{p[0]} - {p[1]}   | corr = {p[2]:.3f}")
