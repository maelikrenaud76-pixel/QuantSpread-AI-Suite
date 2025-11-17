import yfinance as yf
import time
import os
import sys

T1 = "MSFT"
T2 = "AAPL"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

print("Live Monitor running. Press CTRL+C to stop.\n")

last_spread = None

try:
    while True:
        try:
            data = yf.download([T1, T2], period="1d", interval="1m")["Close"].dropna()

            p1 = float(data[T1].iloc[-1])
            p2 = float(data[T2].iloc[-1])
            spread = p1 - p2

            clear()
            print("=== QuantSpread Live Monitor ===")
            print(f"{T1} : {p1:.2f}")
            print(f"{T2} : {p2:.2f}")
            print(f"Spread : {spread:.2f}")

            if last_spread is not None:
                print(f"Δ Spread : {spread - last_spread:+.2f}")

            last_spread = spread

        except Exception as e:
            clear()
            print("⚠ ERREUR DANS LE MONITORING")
            print(str(e))

        print("\nActualisation dans 30 secondes... (CTRL+C pour quitter)")
        time.sleep(30)

except KeyboardInterrupt:
    print("\n\nArrêt demandé par l'utilisateur. Fermeture propre du Live Monitor.")
    sys.exit(0)
