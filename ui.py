import streamlit as st
import plotly.graph_objects as go

def apply_custom_styles():
    st.markdown("""
        <style>
            .stApp { background-color: #0d1117; color: #c9d1d9; }
            .header-container { display: flex; justify-content: space-between; align-items: flex-end; padding-bottom: 20px; border-bottom: 1px solid #30363d; margin-bottom: 20px; }
            .title-section h1 { color: #f0f6fc; margin: 0; font-size: 32px; font-weight: 700; }
            .title-section p { color: #8b949e; margin: 5px 0 0 0; font-size: 14px; }
            
            /* KPI Kartları */
            .kpi-container { display: flex; gap: 15px; }
            .kpi-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px 16px; min-width: 140px; }
            .kpi-label { color: #8b949e; font-size: 10px; font-weight: 600; text-transform: uppercase; margin-bottom: 5px; }
            .kpi-value { color: #c9d1d9; font-size: 16px; font-weight: 600; margin-bottom: 5px; }
            .kpi-subtext { color: #58a6ff; font-size: 11px; }
            .kpi-subtext.benchmark { color: #8b949e; }
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] { gap: 24px; background-color: transparent; }
            .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: transparent; border-radius: 0; border-bottom: 2px solid transparent; color: #8b949e; font-weight: 600; padding: 0 10px; }
            .stTabs [aria-selected="true"] { color: #f85149 !important; border-bottom-color: #f85149 !important; }
        </style>
    """, unsafe_allow_html=True)

def render_kpi_header(df):
    top_rotation = df.sort_values(by="Composite", ascending=False).iloc[0]
    weakening = df.sort_values(by="1W_RS", ascending=True).iloc[0]
    
    emerging = df[(df["1W_RS"] > df["1M_RS"]) & (df["1M_RS"] < 0)].sort_values(by="1W_RS", ascending=False)
    emerging_theme = emerging.iloc[0] if not emerging.empty else df.sort_values(by="1W_RS", ascending=False).iloc[1]
    
    spy_5d = df["SPY_5D_Ret"].iloc[0]

    st.markdown(f"""
        <div class="header-container">
            <div class="title-section">
                <h1>Money Rotation Tracker</h1>
                <p>Theme leadership, relative strength and breadth</p>
            </div>
            <div class="kpi-container">
                <div class="kpi-card">
                    <div class="kpi-label">TOP ROTATION</div>
                    <div class="kpi-value">{top_rotation['Theme']}</div>
                    <div class="kpi-subtext">{top_rotation['Ticker']} (100/100)</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">EMERGING</div>
                    <div class="kpi-value">{emerging_theme['Theme']}</div>
                    <div class="kpi-subtext">{emerging_theme['Ticker']}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">WEAKENING</div>
                    <div class="kpi-value">{weakening['Theme']}</div>
                    <div class="kpi-subtext">{weakening['Ticker']}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">SPY 5D</div>
                    <div class="kpi-value">{spy_5d:+.2f}%</div>
                    <div class="kpi-subtext benchmark">Benchmark</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_chart(df, title, bar_color):
    fig = go.Figure()
    
    if "Composite" in title:
        labels = [f"1M: {ret:+.2f}% | Comp: {rs:+.2f}" for ret, rs in zip(df["Return"], df["RS"])]
    else:
        labels = [f"{ret:+.2f}% | RS: {rs:+.1f}" for ret, rs in zip(df["Return"], df["RS"])]
    
    fig.add_trace(go.Bar(
        x=df["RS"], y=df["Theme"], orientation='h',
        marker=dict(color=bar_color), text=labels, textposition='outside',
        textfont=dict(color='#a0aec0', size=11)
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color="white")),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=max(380, len(df) * 30), margin=dict(l=10, r=100, t=40, b=20),
        xaxis=dict(showgrid=False, zeroline=True, zerolinecolor='#333a4d', showticklabels=False),
        yaxis=dict(showgrid=False, tickfont=dict(color='white', size=12))
    )
    return fig

def render_portfolio_cards(portfolio_df):
    st.markdown("---")
    st.subheader("🎯 Çoklu Zaman Dilimli Dinamik Portföy Dağılımı")
    cols = st.columns(4)
    for i, row in portfolio_df.iterrows():
        with cols[i]:
            st.markdown(f"""
            <div style="background-color: #161b2a; padding: 16px; border-radius: 8px; border-left: 4px solid #4f46e5; margin-bottom: 10px;">
                <span style="font-size: 11px; color: #a0aec0; font-weight: bold; text-transform: uppercase;">{row['Ağırlık']} — {row['Tipi']}</span>
                <h3 style="margin: 6px 0; color: #ffffff; font-size: 20px;">{row['Ticker']}</h3>
                <p style="margin: 0; color: #38bdf8; font-weight: 600; font-size: 13px;">{row['Tema']}</p>
                <p style="margin-top: 8px; font-size: 11px; color: #94a3b8; min-height: 32px;">{row['Açıklama']}</p>
                <span style="font-size: 10px; background-color: #2d3748; padding: 2px 6px; border-radius: 4px; color: #e2e8f0;">Bileşik Skor: {row['Bileşik Skor']}</span>
            </div>
            """, unsafe_allow_html=True)
