import streamlit as st
import yfinance as yf
import plotly.graph_objs as go

# Personal introduction
st.write("**Ruturaj Dilip Gawdae**")
st.write("I am completing my master's in Digital Engineering at OVGU Magdeburg, specializing in Data Science. This app is part of my journey to explore and analyze real-world stock data using data science and visualization tools.")

# Title of the app
st.title("Enhanced Stock Analysis and Prediction App")
st.write("Select a stock from the dropdown or enter any custom ticker to analyze.")

# List of some German stock symbols for predefined options
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
    "1COV.DE": "Covestro AG",
    "MBG.DE": "Mercedes-Benz Group AG",
    "DHER.DE": "Delivery Hero SE",
    "DPW.DE": "Deutsche Post AG",
    "EOAN.DE": "E.ON SE",
    "FME.DE": "Fresenius Medical Care AG",
    "FRE.DE": "Fresenius SE & Co. KGaA",
    "HEI.DE": "HeidelbergCement AG",
    "HEN3.DE": "Henkel AG & Co. KGaA",
    "IFX.DE": "Infineon Technologies AG",
    "LIN.DE": "Linde PLC",
    "MRK.DE": "Merck KGaA",
    "MTX.DE": "MTU Aero Engines AG",
    "MUV2.DE": "Munich Re AG",
    "P911.DE": "Porsche AG",
    "QIA.DE": "Qiagen N.V.",
    "RWE.DE": "RWE AG",
    "SHL.DE": "Siemens Healthineers AG",
    "SY1.DE": "Symrise AG",
    "VNA.DE": "Vonovia SE",
    "ZAL.DE": "Zalando SE",
    "AIR.DE": "Airbus SE",
    "AFX.DE": "Carl Zeiss Meditec AG",
    "FPE3.DE": "Fuchs Petrolub SE",
    "KBX.DE": "Knorr-Bremse AG",
    "LEG.DE": "LEG Immobilien AG",
    "PSM.DE": "ProSiebenSat.1 Media SE",
    "RRTL.DE": "RTL Group",
    "SZU.DE": "Südzucker AG",
    "ENR.DE": "Siemens Energy AG",
    "SIE.DE": "Siemens AG",
    "SRT3.DE": "Sartorius AG",
    "DB1.DE": "Deutsche Börse AG",
    "BOSS.DE": "Hugo Boss AG",
    "TKA.DE": "Thyssenkrupp AG",
    "PUM.DE": "Puma SE",
    "S92.DE": "SMA Solar Technology AG",
    "WDI.DE": "Wirecard AG",
    "HNR1.DE": "Hannover Rück SE",
    "MEO.DE": "MEAG Munich Ergo Kapitalanlagegesellschaft mbH",
    "SAX.DE": "Sachsenmilch AG",
    "KD8.DE": "Kion Group AG",
    "BNR.DE": "Bertrandt AG",
    "G24.DE": "Scout24 AG",
    # Add more predefined German stocks if needed
}

# Initialize session state for managing input fields
if "selected_stock" not in st.session_state:
    st.session_state.selected_stock = ""
if "custom_stock" not in st.session_state:
    st.session_state.custom_stock = ""

# Callback functions to clear fields
def clear_custom_stock():
    st.session_state.custom_stock = ""  # Clear custom ticker if dropdown is used

def clear_selected_stock():
    st.session_state.selected_stock = ""  # Clear dropdown if custom ticker is used

# Dropdown for selecting a predefined stock
selected_stock = st.selectbox("Select a stock:", [""] + list(stock_symbols.keys()), 
                              index=0 if st.session_state.selected_stock == "" else list(stock_symbols.keys()).index(st.session_state.selected_stock) + 1,
                              on_change=clear_custom_stock, key="selected_stock")

# Text input for entering any custom stock ticker
custom_stock = st.text_input("Or type any custom ticker:", value=st.session_state.custom_stock, on_change=clear_selected_stock, key="custom_stock")

# Determine the stock ticker symbol to use
symbol = custom_stock if custom_stock else selected_stock

if symbol:
    try:
        # Fetch stock information
        stock = yf.Ticker(symbol)
        company_name = stock.info.get("shortName", "Unknown Company")
        
        # Display the company name and ticker symbol
        st.write(f"**Analyzing stock:** {company_name} ({symbol})")

        # Fetch stock data for the last 6 months
        stock_data = stock.history(period="6mo", interval="1d")
        if stock_data.empty:
            st.write("No data available for this stock.")
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
    except Exception as e:
        st.write("An error occurred while fetching data for this stock. Please ensure the ticker is correct and try again.")
else:
    st.write("Please select or enter a stock ticker to analyze.")
