import pandas as pd
from datetime import datetime
from config import THEME_MAP, BENCHMARK, MA_PERIOD

def process_theme_metrics(data, timeframe):
    dates = data.index
    today = dates[-1]
    
    # Zaman aralığı bakış penceresi
    if timeframe == "Today":
        start_idx = -2
    elif timeframe == "1W":
        start_idx = -6
    elif timeframe == "1M":
        start_idx = -22
    elif timeframe == "3M":
        start_idx = -66
    elif timeframe == "YTD":
        ytd_start = datetime(today.year, 1, 1)
        start_idx = data.index.get_indexer([ytd_start], method="nearest")[0]
    else:
        start_idx = -2

    spy_data = data[BENCHMARK]
    results = []

    for theme, ticker in THEME_MAP.items():
        if ticker not in data.columns:
            continue
            
        series = data[ticker]
        
        # Yalın Getiri
        ret = ((series.iloc[-1] - series.iloc[start_idx]) / series.iloc[start_idx]) * 100
        
        # Mansfield Relative Strength (RS) Hesabı
        r_series = series / spy_data
        r_sma = r_series.rolling(window=MA_PERIOD).mean()
        mansfield_series = ((r_series / r_sma) - 1) * 100
        mansfield_rs = mansfield_series.iloc[-1]

        results.append({
            "Theme": theme,
            "Ticker": ticker,
            "Return": ret,
            "Mansfield_RS": mansfield_rs
        })
        
    return pd.DataFrame(results)
