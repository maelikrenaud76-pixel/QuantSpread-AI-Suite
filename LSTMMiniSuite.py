# ============================================================
#  LSTMMiniSuite.py  —  QuantSpread AI Mini Analysis Tool
#  Analyse rapide de pair trading : correlation, beta, spread
# ============================================================

import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# 1. PARAMÈTRES
# ------------------------------------------------------------
T1 = "MSFT"
T2 = "AAPL"
START = "2015-01-01"

print("=== QuantSpread AI — MiniSuite ===")
print(f"Analyse rapide de la paire : {T1} / {T2}")
print("-------------------------------------")

# ------------------------------------------------------------
# 2. DOWNLOAD DATA
# ------------------------------------------------------------
data = yf.download([T1, T2], start=START)["Close"].dropna()

returns = data.pct_change().dropna()

# ------------------------------------------------------------
# 3. METRIQUES QUANTITATIVES
# ------------------------------------------------------------
corr = returns[T1].corr(returns[T2])
cov = returns[T1].cov(returns[T2])
var = returns[T2].var()
beta = cov / var

spread = data[T1] - data[T2]
mean_spread = spread.mean()
std_spread = spread.std()

print(f"Correlation            : {corr:.4f}")
print(f"Beta (T1 vs T2)        : {beta:.4f}")
print(f"Spread moyen           : {mean_spread:.2f}")
print(f"Spread écart-type      : {std_spread:.2f}")
print("-------------------------------------")

# Mini diagnostic qualitatif
if corr > 0.8:
    diag = "Excellent candidat pour pairs trading."
elif corr > 0.6:
    diag = "Correct mais volatil."
else:
    diag = "Corrélation faible — risque de divergence."

print("Diagnostic :", diag)

# ------------------------------------------------------------
# 4. PLOTS
# ------------------------------------------------------------

plt.figure(figsize=(12,5))
plt.plot(data[T1], label=T1)
plt.plot(data[T2], label=T2)
plt.title("LSTMMiniSuite — Prix des deux actifs")
plt.grid()
plt.legend()
plt.show()

plt.figure(figsize=(12,5))
plt.plot(spread, label="Spread", color="orange")
plt.axhline(mean_spread, linestyle="--", color="gray", label="Moyenne")
plt.title("LSTMMiniSuite — Spread Historique")
plt.grid()
plt.legend()
plt.show()
