import pandas as pd
from datetime import datetime
from config import THEME_MAP, BENCHMARK, WEIGHT_1W, WEIGHT_1M, WEIGHT_3M

def get_timeframe_index(dates, timeframe):
    today = dates[-1]
    if timeframe == "Today": return -2
    elif timeframe == "1W": return -6
    elif timeframe == "1M": return -22
    elif timeframe == "3M": return -66
    elif timeframe == "YTD":
        ytd_start = datetime(today.year, 1, 1)
        try: return dates.get_indexer([ytd_start], method="nearest")[0]
        except: return -250
    elif timeframe == "1Y":
        one_year_ago = today - pd.DateOffset(years=1)
        try: return dates.get_indexer([one_year_ago], method="nearest")[0]
        except: return -252
    return -2

def process_theme_metrics(data, timeframe):
    dates = data.index
    spy_data = data[BENCHMARK]

    # Tüm zaman dilimleri için indeksleri bul
    idx_1w = get_timeframe_index(dates, "1W")
    idx_1m = get_timeframe_index(dates, "1M")
    idx_3m = get_timeframe_index(dates, "3M")
    idx_ytd = get_timeframe_index(dates, "YTD")
    idx_1y = get_timeframe_index(dates, "1Y")
    
    idx_curr = get_timeframe_index(dates, timeframe if timeframe != "Composite" else "1M")

    # SPY Getirileri
    spy_ret_1w = ((spy_data.iloc[-1] - spy_data.iloc[idx_1w]) / spy_data.iloc[idx_1w]) * 100
    spy_ret_1m = ((spy_data.iloc[-1] - spy_data.iloc[idx_1m]) / spy_data.iloc[idx_1m]) * 100
    spy_ret_3m = ((spy_data.iloc[-1] - spy_data.iloc[idx_3m]) / spy_data.iloc[idx_3m]) * 100
    spy_ret_ytd = ((spy_data.iloc[-1] - spy_data.iloc[idx_ytd]) / spy_data.iloc[idx_ytd]) * 100
    spy_ret_1y = ((spy_data.iloc[-1] - spy_data.iloc[idx_1y]) / spy_data.iloc[idx_1y]) * 100
    spy_ret_curr = ((spy_data.iloc[-1] - spy_data.iloc[idx_curr]) / spy_data.iloc[idx_curr]) * 100

    results = []

    for theme, ticker in THEME_MAP.items():
        if ticker not in data.columns:
            continue
            
        series = data[ticker]
        
        # Seçili zaman dilimi için aktif getiri
        ret_curr = ((series.iloc[-1] - series.iloc[idx_curr]) / series.iloc[idx_curr]) * 100
        rs_curr = ret_curr - spy_ret_curr

        # Matrix için tüm RS'ler
        rs_1w = (((series.iloc[-1] - series.iloc[idx_1w]) / series.iloc[idx_1w]) * 100) - spy_ret_1w
        rs_1m = (((series.iloc[-1] - series.iloc[idx_1m]) / series.iloc[idx_1m]) * 100) - spy_ret_1m
        rs_3m = (((series.iloc[-1] - series.iloc[idx_3m]) / series.iloc[idx_3m]) * 100) - spy_ret_3m
        rs_ytd = (((series.iloc[-1] - series.iloc[idx_ytd]) / series.iloc[idx_ytd]) * 100) - spy_ret_ytd
        rs_1y = (((series.iloc[-1] - series.iloc[idx_1y]) / series.iloc[idx_1y]) * 100) - spy_ret_1y

        # Bileşik Skor (Hızlı Rotasyon Optimizasyonu)
        composite_score = (rs_3m * WEIGHT_3M) + (rs_1m * WEIGHT_1M) + (rs_1w * WEIGHT_1W)

        results.append({
            "Theme": theme,
            "Ticker": ticker,
            "Return": ret_curr,
            "RS": composite_score if timeframe == "Composite" else rs_curr,
            "1W_RS": rs_1w,
            "1M_RS": rs_1m,
            "3M_RS": rs_3m,
            "YTD_RS": rs_ytd,
            "1Y_RS": rs_1y,
            "Composite": composite_score,
            "SPY_5D_Ret": spy_ret_1w # KPI Kartı için
        })
        
    return pd.DataFrame(results)

def generate_portfolio_recommendation(df):
    df_sorted_comp = df.sort_values(by="Composite", ascending=False).reset_index(drop=True)
    portfolio = []
    used_tickers = set()

    if len(df_sorted_comp) > 0:
        core = df_sorted_comp.iloc[0]
        portfolio.append({"Tipi": "Ana Çapa", "Ağırlık": "%35", "Tema": core["Theme"], "Ticker": core["Ticker"], "Bileşik Skor": f"{core['Composite']:+.2f}", "Açıklama": "Uzun vadeli (3M) lider."})
        used_tickers.add(core["Ticker"])

    rem_2 = df_sorted_comp[~df_sorted_comp["Ticker"].isin(used_tickers)]
    rem_2_pos = rem_2[rem_2["1M_RS"] > 0]
    second = rem_2_pos.iloc[0] if not rem_2_pos.empty else (rem_2.iloc[0] if not rem_2.empty else None)
    if second is not None:
        portfolio.append({"Tipi": "İkinci Lider", "Ağırlık": "%30", "Tema": second["Theme"], "Ticker": second["Ticker"], "Bileşik Skor": f"{second['Composite']:+.2f}", "Açıklama": "Orta vadeli destekleyici lider."})
        used_tickers.add(second["Ticker"])

    rem_3 = df.sort_values(by="1W_RS", ascending=False)
    rem_3 = rem_3[~rem_3["Ticker"].isin(used_tickers)]
    if not rem_3.empty:
        tactical = rem_3.iloc[0]
        portfolio.append({"Tipi": "Taktiksel", "Ağırlık": "%20", "Tema": tactical["Theme"], "Ticker": tactical["Ticker"], "Bileşik Skor": f"{tactical['Composite']:+.2f}", "Açıklama": "Kısa vadede (1W) yeni para akışı."})

    portfolio.append({"Tipi": "Risk Koruması", "Ağırlık": "%15", "Tema": "Likit / Nakit", "Ticker": "USD / BIL", "Bileşik Skor": "0.00", "Açıklama": "Rotasyon geçişleri için nakit."})
    return pd.DataFrame(portfolio)
