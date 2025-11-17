# ============================================================================
#  QuantSpread AI Suite  —  Monolithic Edition
#  LSTM-Based Statistical Arbitrage Engine
#  (c) Light & ChatGPT — 2025
# ============================================================================

# ============================================================================
# 1. IMPORTS
# ============================================================================
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

plt.style.use("ggplot")

# ============================================================================
# 2. PARAMETERS (EDITABLE)
# ============================================================================
T1 = "MSFT"
T2 = "AAPL"
START_DATE = "2015-01-01"
SEQ_LEN = 60
THRESHOLD = 0.5   # Sensibilité BUY/SELL

EPOCHS = 20
BATCH = 32

# ============================================================================
# 3. DATA LOADING
# ============================================================================
print("[INFO] Downloading financial data...")
data = yf.download([T1, T2], start=START_DATE)["Close"].dropna()

spread = (data[T1] - data[T2]).values.reshape(-1, 1)

print(f"[DATA] Loaded {len(spread)} datapoints.")

# ============================================================================
# 4. NORMALIZATION
# ============================================================================
print("[INFO] Normalizing spread...")
scaler = MinMaxScaler()
spread_scaled = scaler.fit_transform(spread)

# ============================================================================
# 5. SEQUENCE GENERATION
# ============================================================================
print("[INFO] Generating LSTM sequences...")

X, y = [], []
for i in range(SEQ_LEN, len(spread_scaled)):
    X.append(spread_scaled[i-SEQ_LEN:i])
    y.append(spread_scaled[i])

X, y = np.array(X), np.array(y)

print(f"[SHAPE] X={X.shape}   y={y.shape}")

# ============================================================================
# 6. MODEL CREATION
# ============================================================================
print("[INFO] Building LSTM model...")

model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(SEQ_LEN, 1)),
    Dropout(0.2),
    LSTM(32),
    Dropout(0.2),
    Dense(1)
])

model.compile(optimizer="adam", loss="mse")
model.summary()

# ============================================================================
# 7. TRAINING
# ============================================================================
print("[INFO] Training model...")
model.fit(X, y, epochs=EPOCHS, batch_size=BATCH, validation_split=0.1)

# ============================================================================
# 8. PREDICTION
# ============================================================================
print("[INFO] Predicting spread...")

pred_scaled = model.predict(X)
pred = scaler.inverse_transform(pred_scaled)
real = scaler.inverse_transform(y)

# ============================================================================
# 9. BACKTEST
# ============================================================================
print("[INFO] Running backtest...")

df = pd.DataFrame({
    "real": real.flatten(),
    "pred": pred.flatten(),
    "date": data.index[SEQ_LEN:]
})
df.set_index("date", inplace=True)

df["signal"] = 0
df.loc[df["pred"] > df["real"] + THRESHOLD, "signal"] = -1
df.loc[df["pred"] < df["real"] - THRESHOLD, "signal"] = 1

df["position"] = df["signal"].shift(1).fillna(0)
df["spread_ret"] = df["real"].diff().fillna(0)
df["pnl"] = df["position"] * df["spread_ret"]
df["equity"] = df["pnl"].cumsum()

# ============================================================================
# 10. PERFORMANCE METRICS
# ============================================================================
total_pnl = df["pnl"].sum()
daily_vol = df["pnl"].std()
sharpe = (df["pnl"].mean() / daily_vol) * np.sqrt(252) if daily_vol != 0 else 0

print("\n==================== RESULTS ====================")
print(f"Total PnL      : {total_pnl:.2f} USD (spread units)")
print(f"Sharpe Ratio   : {sharpe:.3f}")
print("=================================================\n")

# ============================================================================
# 11. PLOTS
# ============================================================================
print("[INFO] Plotting results...")

plt.figure(figsize=(13,5))
plt.plot(df.index, df["real"], label="Spread réel", linewidth=1.2)
plt.plot(df.index, df["pred"], label="Spread prédit (LSTM)", linewidth=1)
plt.title("QuantSpread AI Suite — Spread Prediction")
plt.legend(); plt.grid(); plt.show()

plt.figure(figsize=(13,5))
plt.plot(df["equity"], label="Équity Curve", linewidth=1.5)
plt.title("QuantSpread AI Suite — Backtest PnL")
plt.legend(); plt.grid(); plt.show()

print("[DONE] QuantSpread AI Suite completed.")
