import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objs as go

# Title of the app
st.title("Enhanced Stock Analysis and Prediction App")
st.write("Select a stock from the dropdown or search by ticker to analyze.")

# List of stock symbols with their names for predefined options
stock_symbols = {
    "SAP.DE": "SAP SE",
    "DBK.DE": "Deutsche Bank AG",
    "VOW3.DE": "Volkswagen AG",
    "BMW.DE": "BMW AG",
    "DTE.DE": "Deutsche Telekom AG",
    "ALV.DE": "Allianz SE",
    "BAS.DE": "BASF SE",
    "BAYN.DE": "Bayer AG",
    "BEI.DE": "Beiersdorf AG",
    "CON.DE": "Continental AG",
    # Add more predefined German stocks if needed
}

# Initialize session state for managing input fields
if "selected_stock" not in st.session_state:
    st.session_state.selected_stock = ""
if "custom_stock" not in st.session_state:
    st.session_state.custom_stock = ""

# Callback to clear custom_stock if a stock is selected from the dropdown
def on_select_stock():
    st.session_state.custom_stock = ""  # Clear custom stock ticker when dropdown is selected

# Callback to clear selected_stock if a custom ticker is typed in
def on_custom_stock_input():
    st.session_state.selected_stock = ""  # Clear dropdown selection when typing a custom ticker

# Dropdown for selecting predefined stocks
selected_stock = st.selectbox(
    "Select Stock:",
    [""] + list(stock_symbols.keys()),  # Add an empty option for 'unselected' state
    index=0 if st.session_state.selected_stock == "" else list(stock_symbols.keys()).index(st.session_state.selected_stock) + 1,
    on_change=on_select_stock,
)

# Text input for searching by ticker
custom_stock = st.text_input("Search stock with Ticker:", value=st.session_state.custom_stock, on_change=on_custom_stock_input)

# Update session state values
if selected_stock:
    st.session_state.selected_stock = selected_stock
if custom_stock:
    st.session_state.custom_stock = custom_stock

# Determine the stock symbol to use based on user input
symbol = st.session_state.custom_stock if st.session_state.custom_stock else st.session_state.selected_stock
company_name = stock_symbols.get(symbol, "Unknown Company") if not st.session_state.custom_stock else yf.Ticker(symbol).info.get("shortName", "Unknown Company")

# Display the selected stock's name and ticker symbol
if symbol:
    st.write(f"Analyzing stock: {company_name} ({symbol})")

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
        def plot_stock_data(data, symbol, company_name):
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
            fig.add_trace(go.Scatter(x=data.index, y=data['MA50'], mode='lines', name='50-Day MA'))
            fig.add_trace(go.Scatter(x=data.index, y=data['MA200'], mode='lines', name='200-Day MA'))
            fig.update_layout(title=f"{company_name} ({symbol}) - Stock Price with 50-Day and 200-Day Moving Averages",
                              xaxis_title="Date", yaxis_title="Price")
            st.plotly_chart(fig)

        # Plot the stock data with moving averages
        plot_stock_data(stock_data, symbol, company_name)
