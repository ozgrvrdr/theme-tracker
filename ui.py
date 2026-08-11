import streamlit as st
import plotly.graph_objects as go

def apply_custom_styles():
    st.markdown("""
        <style>
            .stApp { 
                background-color: #0b0e14; 
                color: #ffffff; 
            }
            div.stButton > button { 
                background-color: #1a1f2c; 
                color: white; 
                border: 1px solid #333a4d; 
                border-radius: 6px; 
            }
            div.stButton > button:hover { 
                border-color: #4f46e5; 
                color: #4f46e5; 
            }
        </style>
    """, unsafe_allow_html=True)

def render_chart(df, title, bar_color):
    fig = go.Figure()
    
    # Composite görünümü için özel etiket formatı, diğer zaman dilimleri için standart format
    if "Composite" in title:
        labels = [f"1M: {ret:+.2f}% | Comp: {rs:+.2f}" for ret, rs in zip(df["Return"], df["RS"])]
    else:
        labels = [f"{ret:+.2f}% | RS: {rs:+.1f}" for ret, rs in zip(df["Return"], df["RS"])]
    
    fig.add_trace(go.Bar(
        x=df["RS"],
        y=df["Theme"],
        orientation='h',
        marker=dict(color=bar_color),
        text=labels,
        textposition='outside',
        textfont=dict(color='#a0aec0', size=11)
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color="white")),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=max(380, len(df) * 30),
        margin=dict(l=10, r=100, t=40, b=20),
        xaxis=dict(showgrid=False, zeroline=True, zerolinecolor='#333a4d', showticklabels=False),
        yaxis=dict(showgrid=False, tickfont=dict(color='white', size=12))
    )
    return fig

def render_portfolio_cards(portfolio_df):
    st.markdown("---")
    st.subheader("🎯 Çoklu Zaman Dilimli Dinamik Portföy Dağılımı")
    st.caption("Piyasa verilerine göre otomatik güncellenen 4 parçalı tema modeli")
    
    cols = st.columns(4)
    for i, row in portfolio_df.iterrows():
        with cols[i]:
            st.markdown(f"""
            <div style="background-color: #161b2a; padding: 16px; border-radius: 8px; border-left: 4px solid #4f46e5; margin-bottom: 10px;">
                <span style="font-size: 11px; color: #a0aec0; font-weight: bold; text-transform: uppercase;">{row['Ağırlık']} — {row['Tipi']}</span>
                <h3 style="margin: 6px 0; color: #ffffff; font-size: 20px;">{row['Ticker']}</h3>
                <p style="margin: 0; color: #38bdf8; font-weight: 600; font-size: 13px;">{row['Tema']}</p>
                <p style="margin-top: 8px; font-size: 11px; color: #94a3b8; min-height: 32px;">{row['Açıklama']}</p>
                <span style="font-size: 10px; background-color: #2d3748; padding: 2px 6px; border-radius: 4px; color: #e2e8f0;">Bileşik RS: {row['Bileşik Skor']}</span>
            </div>
            """, unsafe_allow_html=True)
