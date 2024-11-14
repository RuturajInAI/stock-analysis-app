
# Enhanced Stock Analysis and Prediction App

This Streamlit-based application allows users to analyze German stock market data using historical trends and basic technical indicators. The app provides a simple recommendation (Buy, Not Buy, or Hold) based on calculated moving averages and the Relative Strength Index (RSI).

## Features

- **Stock Selection**: Choose from a dropdown list of predefined German stocks or enter any custom stock ticker.
- **Historical Data Visualization**: Display the stock's closing prices with 50-day and 200-day moving averages over the last 6 months.
- **Technical Analysis-Based Recommendation**: Get a recommendation based on moving averages and RSI.
- **User-Friendly Interface**: Built with Streamlit for ease of use and real-time interaction.

## Technical Indicators Used

1. **Moving Averages (MA50 and MA200)**:
   - The 50-day moving average (MA50) reflects short-term trends.
   - The 200-day moving average (MA200) reflects longer-term trends.
   - If MA50 is above MA200, it suggests an uptrend, while MA50 below MA200 suggests a downtrend.

2. **Relative Strength Index (RSI)**:
   - The RSI is a momentum oscillator that helps identify overbought or oversold conditions.
   - RSI above 70 suggests overbought conditions (potential for a price drop).
   - RSI below 30 suggests oversold conditions (potential for a price increase).

## Prediction Logic

The app uses a rule-based approach for predictions:

- **Buy**: Recommended when MA50 > MA200 and RSI < 70.
- **Not Buy**: Recommended when MA50 < MA200 and RSI > 30.
- **Hold**: Suggested if the trend is unclear or indicators are mixed.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/stock-analysis-app.git
   cd stock-analysis-app
   ```

2. **Install Dependencies**:
   Make sure you have Python and pip installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   streamlit run stock_analysis_app.py
   ```

## How to Use

1. **Select a Stock**:
   - Choose from a list of predefined German stocks in the dropdown menu, or type any valid stock ticker in the text input.
   
2. **View Analysis**:
   - The app will fetch the last 6 months of stock data, display a graph with 50-day and 200-day moving averages, and provide a technical analysis-based recommendation.

3. **Interpret the Prediction**:
   - The prediction is color-coded for easy interpretation:
     - **Green**: Buy recommendation
     - **Red**: Not Buy recommendation
     - **Gray**: Hold recommendation

## Example Stocks

- Popular German stocks included: SAP (SAP.DE), Deutsche Bank (DBK.DE), Volkswagen (VOW3.DE), and others.
- You can also analyze custom tickers by typing in a valid stock symbol.

## Project Motivation

This app was developed by **Ruturaj Dilip Gawdae** as part of a learning project in Digital Engineering and Data Science. It serves as a practical application of stock data analysis using basic indicators, providing users with insights into real-time stock trends and technical analysis.

## License

This project is open-source and available under the MIT License.
