import vectorbtpro as vbt

DB_PATH = "../forex_market.duckdb"
symbol = "EURUSD"
data = vbt.DuckDBData.from_duckdb(symbol, start="2013-01-01", connection=DB_PATH)
close = data.close

window = 20
wtype = "simple"
alpha = 2
minp = 1
adjust = True
ddof = 0
bb = vbt.BBANDS.run(close, window=window, wtype=wtype, alpha=alpha, minp=minp, adjust=adjust, ddof=ddof)
bandwidth = bb.bandwidth
percent_b = bb.percent_b

print(bandwidth)
print(percent_b)
