import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objs as go

# Title of the app
st.title("Enhanced Stock Analysis and Prediction App")
st.write("Select a stock from the dropdown or enter a custom ticker to analyze.")

# Expanded list of German stock symbols with their names for predefined options
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

# Combine the list of stocks with an empty entry for custom tickers
stock_options = [""] + [f"{ticker} - {name}" for ticker, name in stock_symbols.items()]

# Initialize session state for managing input field
if "stock_input" not in st.session_state:
    st.session_state.stock_input = ""

# Callback to handle selection and manual entry
def on_stock_select():
    st.session_state.stock_input = st.session_state.stock_dropdown.split(" - ")[0]  # Set stock_input to ticker only

# Dropdown/search field for selecting or entering a stock ticker
st.write("Select a stock or enter a custom ticker:")
stock_dropdown = st.selectbox(" ", stock_options, index=0, on_change=on_stock_select, key="stock_dropdown")

# Determine the stock symbol to use
if st.session_state.stock_input and st.session_state.stock_input not in stock_symbols:
    symbol = st.session_state.stock_input  # Use custom ticker entered by user
    company_name = yf.Ticker(symbol).info.get("shortName", "Unknown Company")
else:
    symbol = stock_dropdown.split(" - ")[0] if stock_dropdown else ""
    company_name = stock_symbols.get(symbol, "Unknown Company")

# Display the selected stock's name and ticker symbol
if symbol:
    st.write(f"**Analyzing stock:** {company_name} ({symbol})")

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

            # Recommendation based on trend and RSI
            if latest_ma50 > latest_ma200 and latest_rsi < 70:
                return "Uptrend likely to continue - Recommendation: Buy", "green"
            elif latest_ma50 < latest_ma200 and latest_rsi > 30:
                return "Downtrend likely to continue - Recommendation: Not Buy", "red"
            else:
                return "Trend is unclear - Recommendation: Hold", "gray"

        # Show the prediction with color-coded text
        prediction, color = analyze_and_predict(stock_data)
        st.markdown(f"<span style='color:{color}; font-weight:bold;'>Prediction: {prediction}</span>", unsafe_allow_html=True)

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

        # Display the last 6 months of data in a table
        st.write("**Last 6 Months of Data:**")
        st.dataframe(stock_data)
