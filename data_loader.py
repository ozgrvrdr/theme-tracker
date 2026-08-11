import streamlit as st
import yfinance as yf
from config import BENCHMARK

@st.cache_data(ttl=1800)  # Verileri 30 dakika hafızada tutar (Ön-bellek)
def fetch_market_data(tickers):
    all_tickers = list(set(tickers + [BENCHMARK]))
    data = yf.download(all_tickers, period="2y", interval="1d", progress=False)["Close"]
    return data
