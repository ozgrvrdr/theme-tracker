import streamlit as st
from config import THEME_MAP
from data_loader import fetch_market_data
from analytics import process_theme_metrics, generate_portfolio_recommendation
from ui import apply_custom_styles, render_chart, render_portfolio_cards, render_kpi_header

st.set_page_config(page_title="Money Rotation Tracker", layout="wide", initial_sidebar_state="collapsed")
apply_custom_styles()

# Veri yükleme
tickers = list(THEME_MAP.values())
raw_data = fetch_market_data(tickers)

# Tüm metriklerin hesaplanması
# Sadece KPI için ilk başta geçici bir "1M" df'si yaratıyoruz
df_base = process_theme_metrics(raw_data, "1M")

# Üst Header ve KPI Kartları
render_kpi_header(df_base)

# Sekmelerin (Tabs) Oluşturulması
tab1, tab2 = st.tabs(["Visual Theme Tracker", "RS Strength Matrix"])

with tab1:
    # 1Y Seçeneği eklendi
    timeframe = st.radio("Timeframe Selection", options=["Composite", "Today", "1W", "1M", "3M", "YTD", "1Y"], horizontal=True)
    
    # Seçilen zaman dilimine göre veriyi güncelle
    df_metrics = process_theme_metrics(raw_data, timeframe)
    
    # Güçlü ve zayıf temaları ayırma
    df_strength = df_metrics[df_metrics["RS"] >= 0].sort_values(by="RS", ascending=True)
    df_weakness = df_metrics[df_metrics["RS"] < 0].sort_values(by="RS", ascending=False)
    
    col1, col2 = st.columns(2)
    with col1:
        if not df_strength.empty:
            # Yeşil renk kodu (#2ea043)
            st.plotly_chart(render_chart(df_strength, f"Strength (RS > 0) [{timeframe}]", "#2ea043"), use_container_width=True)
    with col2:
        if not df_weakness.empty:
            # Kırmızı renk kodu (#f85149)
            st.plotly_chart(render_chart(df_weakness, f"Weakness (RS < 0) [{timeframe}]", "#f85149"), use_container_width=True)
            
    # Dinamik Portföy Dağılım Kartları
    portfolio_df = generate_portfolio_recommendation(df_metrics)
    render_portfolio_cards(portfolio_df)

with tab2:
    st.markdown("### RS Strength Matrix (Relative Strength Scoreboard)")
    
    # Akıllı Filtreleme Seçenekleri (Erken Uyarı Sistemi)
    filter_option = st.radio(
        "Erken Uyarı Filtresi:",
        options=["Tüm Temalar", "Dipten Dönüş Yapanlar (Emerging)", "İvme Kaybedenler (Weakening)"],
        horizontal=True
    )
    
    display_cols = ["Theme", "Ticker", "1W_RS", "1M_RS", "3M_RS", "YTD_RS", "1Y_RS", "Composite"]
    df_display = df_base.copy()
    
    # Filtreleme Mantığı
    if filter_option == "Dipten Dönüş Yapanlar (Emerging)":
        # 1 Haftalık RS'i pozitifleşen ve 1 Aylık RS'inden büyük olan, ama genel 1 Aylık RS'i hala negatif olanlar
        df_display = df_display[(df_display["1W_RS"] > df_display["1M_RS"]) & (df_display["1M_RS"] < 0)]
    elif filter_option == "İvme Kaybedenler (Weakening)":
        # 1 Aylık RS'i pozitif olup iyi giderken, son 1 Haftalık RS'i negatife dönenler
        df_display = df_display[(df_display["1W_RS"] < 0) & (df_display["1M_RS"] > 0)]
        
    df_display = df_display.sort_values(by="Composite", ascending=False)[display_cols]
    
    # Pandas Styler ile ısı haritası
    styled_df = df_display.style.background_gradient(
        cmap="RdYlGn", 
        subset=["1W_RS", "1M_RS", "3M_RS", "YTD_RS", "1Y_RS", "Composite"]
    ).format({
        "1W_RS": "{:.2f}", "1M_RS": "{:.2f}", "3M_RS": "{:.2f}", 
        "YTD_RS": "{:.2f}", "1Y_RS": "{:.2f}", "Composite": "{:.2f}"
    })
    
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
