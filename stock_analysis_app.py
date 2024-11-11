import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objs as go

# Title of the app
st.title("Enhanced Stock Analysis and Prediction App")
st.write("Select a stock from the dropdown or type a stock symbol to analyze.")

# List of common German stock symbols
stock_symbols = ["SAP.DE", "DBK.DE", "VOW3.DE", "BMW.DE", "DTE.DE"]

# Dropdown and text input for selecting a stock
selected_stock = st.selectbox("Select Stock:", stock_symbols)
custom_stock = st.text_input("Or type a custom stock symbol:")

# Decide which stock to use based on user input
symbol = custom_stock if custom_stock else selected_stock
st.write(f"Analyzing stock: {symbol}")

# Function to fetch stock data for the last 6 months
def fetch_last_6_months_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="6mo", interval="1d")
    return data

# Fetch the last 6 months of data
stock_data = fetch_last_6_months_data(symbol)
if stock_data.empty:
    st.write("Data unavailable for this stock.")
else:
    st.write("Last 6 Months of Data:")
    st.dataframe(stock_data)

    # Function to analyze the stock and make a trend-based prediction
    def analyze_and_predict(data):
        # Calculate 50-day and 200-day moving averages for trend analysis
        data['MA50'] = data['Close'].rolling(window=50, min_periods=1).mean()
        data['MA200'] = data['Close'].rolling(window=200, min_periods=1).mean()

        # Calculate 10-day RSI for additional insight
        delta = data['Close'].diff(1)
        gain = (delta.where(delta > 0, 0)).rolling(window=14, min_periods=1).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14, min_periods=1).mean()
        RS = gain / loss
        data['RSI'] = 100 - (100 / (1 + RS))

        # Check trend based on moving averages
        latest_close = data['Close'].iloc[-1]
        latest_ma50 = data['MA50'].iloc[-1]
        latest_ma200 = data['MA200'].iloc[-1]
        latest_rsi = data['RSI'].iloc[-1]

        # Simple prediction logic based on trend
        if latest_ma50 > latest_ma200 and latest_rsi < 70:
            prediction = "Uptrend likely to continue - Recommendation: Buy"
        elif latest_ma50 < latest_ma200 and latest_rsi > 30:
            prediction = "Downtrend likely to continue - Recommendation: Sell"
        else:
            prediction = "Trend is unclear - Hold recommendation"

        return prediction

    # Show the prediction
    prediction = analyze_and_predict(stock_data)
    st.write(f"Prediction: **{prediction}**")

    # Function to plot the stock data with moving averages
    def plot_stock_data(data, symbol):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
        fig.add_trace(go.Scatter(x=data.index, y=data['MA50'], mode='lines', name='50-Day MA'))
        fig.add_trace(go.Scatter(x=data.index, y=data['MA200'], mode='lines', name='200-Day MA'))
        fig.update_layout(title=f"{symbol} Stock Price with 50-Day and 200-Day Moving Averages",
                          xaxis_title="Date", yaxis_title="Price")
        st.plotly_chart(fig)

    # Plot the stock data with moving averages
    plot_stock_data(stock_data, symbol)
