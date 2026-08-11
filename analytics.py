import pandas as pd
from datetime import datetime
from config import THEME_MAP, BENCHMARK, MA_PERIOD

def get_timeframe_index(dates, timeframe):
    today = dates[-1]
    if timeframe == "Today":
        return -2
    elif timeframe == "1W":
        return -6
    elif timeframe == "1M":
        return -22
    elif timeframe == "3M":
        return -66
    elif timeframe == "YTD":
        ytd_start = datetime(today.year, 1, 1)
        try:
            return dates.get_indexer([ytd_start], method="nearest")[0]
        except:
            return -250
    return -2

def process_theme_metrics(data, timeframe):
    dates = data.index
    spy_data = data[BENCHMARK]

    # Farklı zaman dilimleri için indeksler
    idx_3m = get_timeframe_index(dates, "3M")
    idx_1m = get_timeframe_index(dates, "1M")
    idx_1w = get_timeframe_index(dates, "1W")
    idx_curr = get_timeframe_index(dates, timeframe if timeframe != "Composite" else "1M")

    # SPY Getirileri
    spy_ret_3m = ((spy_data.iloc[-1] - spy_data.iloc[idx_3m]) / spy_data.iloc[idx_3m]) * 100
    spy_ret_1m = ((spy_data.iloc[-1] - spy_data.iloc[idx_1m]) / spy_data.iloc[idx_1m]) * 100
    spy_ret_1w = ((spy_data.iloc[-1] - spy_data.iloc[idx_1w]) / spy_data.iloc[idx_1w]) * 100
    spy_ret_curr = ((spy_data.iloc[-1] - spy_data.iloc[idx_curr]) / spy_data.iloc[idx_curr]) * 100

    results = []

    for theme, ticker in THEME_MAP.items():
        if ticker not in data.columns:
            continue
            
        series = data[ticker]
        
        # Nominal ve Bağıl Getiriler (RS)
        ret_curr = ((series.iloc[-1] - series.iloc[idx_curr]) / series.iloc[idx_curr]) * 100
        rs_curr = ret_curr - spy_ret_curr

        rs_3m = (((series.iloc[-1] - series.iloc[idx_3m]) / series.iloc[idx_3m]) * 100) - spy_ret_3m
        rs_1m = (((series.iloc[-1] - series.iloc[idx_1m]) / series.iloc[idx_1m]) * 100) - spy_ret_1m
        rs_1w = (((series.iloc[-1] - series.iloc[idx_1w]) / series.iloc[idx_1w]) * 100) - spy_ret_1w

        # Bileşik Skor Hesaplaması: 3M (%40) + 1M (%40) + 1W (%20)
        composite_score = (rs_3m * 0.40) + (rs_1m * 0.40) + (rs_1w * 0.20)

        results.append({
            "Theme": theme,
            "Ticker": ticker,
            "Return": ret_curr,
            "RS": composite_score if timeframe == "Composite" else rs_curr,
            "RS_3M": rs_3m,
            "RS_1M": rs_1m,
            "RS_1W": rs_1w,
            "Composite_Score": composite_score
        })
        
    return pd.DataFrame(results)

def generate_portfolio_recommendation(df):
    """
    Çoklu Zaman Dilimli Portföy Dağılım Modeli
    """
    df_sorted_comp = df.sort_values(by="Composite_Score", ascending=False).reset_index(drop=True)
    
    portfolio = []
    used_tickers = set()

    # 1. Ana Çapa (%35)
    if len(df_sorted_comp) > 0:
        core = df_sorted_comp.iloc[0]
        portfolio.append({
            "Tipi": "Ana Çapa (Core Leader)",
            "Ağırlık": "%35",
            "Tema": core["Theme"],
            "Ticker": core["Ticker"],
            "Bileşik Skor": f"{core['Composite_Score']:+.2f}",
            "Açıklama": "Uzun vadeli (3M) lider ve trendin ana omurgası."
        })
        used_tickers.add(core["Ticker"])

    # 2. İkinci Lider (%30)
    rem_2 = df_sorted_comp[~df_sorted_comp["Ticker"].isin(used_tickers)]
    rem_2_pos = rem_2[rem_2["RS_1M"] > 0]
    second = rem_2_pos.iloc[0] if not rem_2_pos.empty else (rem_2.iloc[0] if not rem_2.empty else None)

    if second is not None:
        portfolio.append({
            "Tipi": "İkinci Lider (Trend Support)",
            "Ağırlık": "%30",
            "Tema": second["Theme"],
            "Ticker": second["Ticker"],
            "Bileşik Skor": f"{second['Composite_Score']:+.2f}",
            "Açıklama": "Güçlü orta vadeli momentum sağlayan destekleyici lider."
        })
        used_tickers.add(second["Ticker"])

    # 3. Taktiksel / İvme Kazanan (%20)
    rem_3 = df.sort_values(by="RS_1W", ascending=False)
    rem_3 = rem_3[~rem_3["Ticker"].isin(used_tickers)]
    if not rem_3.empty:
        tactical = rem_3.iloc[0]
        portfolio.append({
            "Tipi": "Taktiksel / İvme Kazanan (Tactical)",
            "Ağırlık": "%20",
            "Tema": tactical["Theme"],
            "Ticker": tactical["Ticker"],
            "Bileşik Skor": f"{tactical['Composite_Score']:+.2f}",
            "Açıklama": "Kısa vadede (1W) yeni para akışı ve ivme kazanan tema."
        })
        used_tickers.add(tactical["Ticker"])

    # 4. Nakit / Risk Koruması (%15)
    portfolio.append({
        "Tipi": "Risk / Nakit Koruması (Cash)",
        "Ağırlık": "%15",
        "Tema": "Likit Portföy / Nakit",
        "Ticker": "USD / BIL",
        "Bileşik Skor": "0.00",
        "Açıklama": "Rotasyon geçişleri ve düzeltmeler için korumalı nakit payı."
    })

    return pd.DataFrame(portfolio)
