import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Stock & Crypto Dashboard", layout="wide")
st.title("📊 StockCrypto Dashboard ")

# Sidebar: Market & Assets
market = st.sidebar.radio("Select Market", ["Stocks", "Cryptocurrency"])

# List CSV files
data_files = os.listdir("data")
if market == "Stocks":
    csv_options = [f for f in data_files if "-" not in f and f.endswith(".csv")]
else:
    csv_options = [f for f in data_files if "-" in f and f.endswith(".csv")]

file_selected = st.sidebar.selectbox("Select Asset", csv_options)

# Load CSV
data = pd.read_csv(f"data/{file_selected}", index_col=0, parse_dates=True)

# Standardize columns
rename_dict = {}
for col in data.columns:
    col_clean = col.lower().strip().replace(" ", "_").replace(".", "")
    if "close" in col_clean:
        rename_dict[col] = "Close"
    elif "open" in col_clean:
        rename_dict[col] = "Open"
    elif "high" in col_clean:
        rename_dict[col] = "High"
    elif "low" in col_clean:
        rename_dict[col] = "Low"
    elif "volume" in col_clean:
        rename_dict[col] = "Volume"
    elif "marketcap" in col_clean or "market_cap" in col_clean:
        rename_dict[col] = "MarketCap"
data.rename(columns=rename_dict, inplace=True)

# Date Filter
st.sidebar.subheader("Filter by Date")
min_date = data.index.min().date()
max_date = data.index.max().date()

start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

# Filter the dataframe
data_filtered = data.loc[(data.index.date >= start_date) & (data.index.date <= end_date)]

# Data Preview
st.subheader(f"📑 {file_selected} Data Preview")
st.dataframe(data_filtered.head())

# Closing Price Chart
if "Close" in data_filtered.columns:
    st.subheader("📈 Price Chart")
    fig = px.line(data_filtered, x=data_filtered.index, y="Close", title=f"{file_selected} Prices Over Time")
    st.plotly_chart(fig, use_container_width=True)

    # Moving Averages
    st.subheader("📊 Moving Averages")
    data_filtered["MA50"] = data_filtered["Close"].rolling(50).mean()
    data_filtered["MA200"] = data_filtered["Close"].rolling(200).mean()
    fig2 = px.line(data_filtered, x=data_filtered.index, y=["Close", "MA50", "MA200"],
                   title=f"{file_selected} with Moving Averages")
    st.plotly_chart(fig2, use_container_width=True)

    # Returns Distribution
    st.subheader("📊 Daily Returns Distribution")
    data_filtered["Returns"] = data_filtered["Close"].pct_change()
    fig3 = px.histogram(data_filtered, x="Returns", nbins=50,
                        title=f"{file_selected} Daily Returns Distribution")
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.error(f"'Close' column not found. Available columns: {data_filtered.columns}")
