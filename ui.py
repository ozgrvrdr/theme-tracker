import streamlit as st
import plotly.graph_objects as go

def apply_custom_styles():
    st.markdown("""
        <style>
            .stApp { background-color: #0b0e14; color: #ffffff; }
            div.stButton > button { background-color: #1a1f2c; color: white; border: 1px solid #333a4d; border-radius: 6px; }
            div.stButton > button:hover { border-color: #4f46e5; color: #4f46e5; }
        </style>
    """, unsafe_allow_html=True)

def render_chart(df, title, bar_color):
    fig = go.Figure()
    # Etikette Nominal Getiri ve Seçilen Zaman Diliminin RS Değeri Gösterilir
    labels = [f"{ret:+.2f}% | RS: {rs:+.1f}" for ret, rs in zip(df["Return"], df["RS"])]
    
    fig.add_trace(go.Bar(
        x=df["RS"],  # Bar uzunlukları dinamik zaman dilimi RS değerine bağlandı
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
