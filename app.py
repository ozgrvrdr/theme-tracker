import streamlit as st
from config import THEME_MAP
from data_loader import fetch_market_data
from analytics import process_theme_metrics
from ui import apply_custom_styles, render_chart

st.set_page_config(page_title="Visual Theme Tracker", layout="wide", initial_sidebar_state="collapsed")
apply_custom_styles()

st.title("Visual Theme Tracker")

# Zaman dilimi seçici
timeframe = st.radio("Timeframe", options=["Today", "1W", "1M", "3M", "YTD"], horizontal=True)

# Veri yükleme ve işleme
tickers = list(THEME_MAP.values())
raw_data = fetch_market_data(tickers)
df_metrics = process_theme_metrics(raw_data, timeframe)

# Dinamik Zaman Dilimi RS Değerine Göre Yeniden Sıralama (Re-sort)
df_strength = df_metrics[df_metrics["RS"] >= 0].sort_values(by="RS", ascending=True)
df_weakness = df_metrics[df_metrics["RS"] < 0].sort_values(by="RS", ascending=False)

# İki sütunlu görünüm
col1, col2 = st.columns(2)

with col1:
    if not df_strength.empty:
        st.plotly_chart(render_chart(df_strength, "Strength (RS > 0)", "#3b82f6"), use_container_width=True)

with col2:
    if not df_weakness.empty:
        st.plotly_chart(render_chart(df_weakness, "Weakness (RS < 0)", "#ec4899"), use_container_width=True)
