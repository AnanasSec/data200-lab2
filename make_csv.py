import yfinance as yf

# 5 years of NVDA history, written in Yahoo CSV format
df = yf.download("NVDA", start="2021-05-01", end="2026-05-01", auto_adjust=False)

# Flatten yfinance's multi-level columns
df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]

# Reorder/rename to match Yahoo's exact CSV layout
df = df[["Open", "High", "Low", "Close", "Adj Close", "Volume"]]
df.index.name = "Date"
df.to_csv("NVDA.csv", date_format="%Y-%m-%d")

print(f"Wrote NVDA.csv with {len(df)} rows")