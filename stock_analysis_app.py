import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objs as go

# Title of the app
st.title("Stock Analysis App")
st.write("Select a stock from the dropdown or type a stock symbol to analyze.")

# List of common German stock symbols
stock_symbols = ["SAP.DE", "DBK.DE", "VOW3.DE", "BMW.DE", "DTE.DE"]

# Dropdown and text input for selecting a stock
selected_stock = st.selectbox("Select Stock:", stock_symbols)
custom_stock = st.text_input("Or type a custom stock symbol:")

# Decide which stock to use based on user input
symbol = custom_stock if custom_stock else selected_stock
st.write(f"Analyzing stock: {symbol}")

# Function to fetch stock data for the last month and display the last 10 days
def fetch_last_10_days_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1mo", interval="1d")
    # Take only the last 10 rows if there is more than 10 days of data
    if len(data) > 10:
        data = data.tail(10)
    return data

# Fetch the last month of data and display the last 10 days
stock_data = fetch_last_10_days_data(symbol)
if stock_data.empty:
    st.write("Data unavailable for this stock.")
else:
    st.write("Last 10 Days of Data:")
    st.dataframe(stock_data)

    # Function to analyze the stock and give a recommendation
    def analyze_stock(data):
        # Check if there's enough data for calculation
        if data.empty:
            return "Data unavailable for this stock."

        # Calculate 10-day moving average
        data['MA10'] = data['Close'].rolling(window=10).mean()
        
        # Calculate RSI (Relative Strength Index)
        delta = data['Close'].diff(1)
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        RS = gain / loss
        data['RSI'] = 100 - (100 / (1 + RS))

        # Check if we have enough data points to calculate indicators
        if data['MA10'].isna().all() or data['RSI'].isna().all():
            return "Insufficient data to make a recommendation."

        # Decision based on the latest closing price and indicators
        latest_close = data['Close'].iloc[-1]
        latest_ma10 = data['MA10'].iloc[-1]
        latest_rsi = data['RSI'].iloc[-1]

        if latest_close > latest_ma10 and latest_rsi < 30:
            return "Buy"
        else:
            return "Not Buy"

    # Show the recommendation
    suggestion = analyze_stock(stock_data)
    st.write(f"Recommendation: **{suggestion}**")

    # Function to plot the stock data with moving average
    def plot_stock_data(data, symbol):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
        fig.add_trace(go.Scatter(x=data.index, y=data['MA10'], mode='lines', name='10-Day MA'))
        fig.update_layout(title=f"{symbol} Stock Price with 10-Day Moving Average",
                          xaxis_title="Date", yaxis_title="Price")
        st.plotly_chart(fig)

    # Plot the stock data
    plot_stock_data(stock_data, symbol)
