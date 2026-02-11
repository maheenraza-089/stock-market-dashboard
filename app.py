import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

# 1. MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(layout="wide", page_title="Stock Peer Analysis")

# Load datasets
# Note: Ensure these files are in the same folder as your script
df_apple = pd.read_csv('AAPL.csv')
df_netflix = pd.read_csv('NFLX.csv')

df_apple['source'] = 'AAPL'
df_netflix['source'] = 'NFLX'

# Concatenate them vertically
df_combined = pd.concat([df_apple, df_netflix], axis=0)
df_combined['Date'] = pd.to_datetime(df_combined['Date'])

def set_dark_theme():
    st.markdown(
        """
        <style>
        .stApp { background-color: #0b1425; color: white; }
        [data-testid="stSidebar"] { background-color: #111b2e; }
        div[data-testid="stVerticalBlock"] > div:has(div.stPlotlyChart) {
            background-color: #162238;
            border-radius: 10px;
            padding: 15px;
        }
        h1, h2, h3, p { color: #e0e0e0; }
        </style>
        """,
        unsafe_allow_html=True
    )

set_dark_theme()

st.title("📈 Stock Peer Analysis")

# --- SIDEBAR / FILTERS ---
st.sidebar.header("Configuration")
tickers = st.sidebar.multiselect("Select Tickers", options=['AAPL', 'NFLX'], default=['AAPL', 'NFLX'])
time_horizon = st.sidebar.radio("Time Horizon", ["1 Month", "6 Months", "1 Year"])

# Filter data
df_filtered = df_combined[df_combined['source'].isin(tickers)]

# --- MAIN DASHBOARD ---
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Performance Summary")
    st.metric(label="Best Stock", value="AAPL", delta="165%")
    st.metric(label="Worst Stock", value="NFLX", delta="-12%", delta_color="inverse")

with col2:
    st.subheader("Normalized Price Comparison")
    # CHANGED 'Price' to 'Close' here
    fig = px.line(df_filtered, x='Date', y='Close', color='source', 
                  template="plotly_dark", labels={'Close': 'Price'})
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

# --- INDIVIDUAL COMPARISON ---
st.markdown("---")
st.subheader("Individual Stocks vs Peer Average")

c_a, c_b, c_c, c_d = st.columns(4)
# Use 'Close' consistently here as well
c_a.line_chart(df_apple.set_index('Date')['Close'])
c_b.area_chart(df_apple.set_index('Date')['Close'].pct_change())