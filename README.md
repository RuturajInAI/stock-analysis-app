# Stock Analysis App

This project is an interactive **Stock Analysis App** built using Streamlit. The app fetches real-time stock data for the last 10 days, performs basic analysis, and provides a recommendation on whether to "Buy" or "Not Buy" the selected stock. The app also includes an interactive chart displaying the stock's recent performance.

## Features

- Fetches the last 10 days of stock data for a selected stock.
- Provides a simple "Buy" or "Not Buy" recommendation based on stock trends.
- Visualizes the stock's closing prices and 10-day moving average in an interactive chart.
- Allows the user to select a stock from a predefined list or type a custom stock symbol.

## How to Use the App

1. Select a stock from the dropdown menu or type a custom stock symbol.
2. The app will fetch and display the last 10 days of data for the selected stock.
3. A recommendation to "Buy" or "Not Buy" the stock will be shown based on recent performance.
4. An interactive chart visualizing the stock price and 10-day moving average is also provided.

## Technology Stack

- **Python**: The programming language used for the entire project.
- **Streamlit**: Used to create the interactive web interface.
- **yfinance**: Fetches the stock data from Yahoo Finance.
- **pandas**: For data manipulation and calculations.
- **plotly**: For creating interactive charts.

## How It Works

1. **Fetch Data**: The app uses `yfinance` to get stock data from Yahoo Finance for the last 10 days.
2. **Analyze Data**: It calculates a 10-day moving average and Relative Strength Index (RSI) to determine stock performance.
   - **Buy** if the closing price is above the 10-day moving average and the RSI is low (indicating the stock is oversold).
   - **Not Buy** otherwise.
3. **Display Results**: The app shows the stock data, recommendation, and an interactive chart.

## Setup and Deployment

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/stock-analysis-app.git
   cd stock-analysis-app
