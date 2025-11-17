import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# ============================================================
# 1. LOAD DATA
# ============================================================
T1 = "MSFT"
T2 = "AAPL"

data = yf.download([T1, T2], start="2015-01-01")["Close"].dropna()
spread = data[T1] - data[T2]

# ============================================================
# 2. BASIC STATISTICS
# ============================================================
mean_spread = spread.mean()
std_spread = spread.std()
min_spread = spread.min()
max_spread = spread.max()

# ============================================================
# 3. PLOT CHART
# ============================================================
plt.figure(figsize=(10,4))
plt.plot(spread, label="Spread")
plt.axhline(mean_spread, color="black", linestyle="--", label="Mean")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("spread_chart.png")
plt.close()

# ============================================================
# 4. GENERATE PDF REPORT
# ============================================================
pdf = FPDF()
pdf.add_page()

pdf.set_font("Arial", size=16)
pdf.cell(0, 10, "QuantSpread AI Suite - Financial Report", ln=True)

pdf.set_font("Arial", size=12)
pdf.ln(5)

pdf.cell(0, 8, f"Asset 1 : {T1}", ln=True)
pdf.cell(0, 8, f"Asset 2 : {T2}", ln=True)
pdf.ln(5)

pdf.cell(0, 8, f"Spread mean       : {mean_spread:.2f}", ln=True)
pdf.cell(0, 8, f"Spread std        : {std_spread:.2f}", ln=True)
pdf.cell(0, 8, f"Spread min        : {min_spread:.2f}", ln=True)
pdf.cell(0, 8, f"Spread max        : {max_spread:.2f}", ln=True)

pdf.ln(10)
pdf.cell(0, 8, "Spread Chart:", ln=True)
pdf.image("spread_chart.png", w=180)

pdf.output("QuantReport.pdf")

print("PDF generated: QuantReport.pdf")
