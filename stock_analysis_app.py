import streamlit as st
import yfinance as yf
import plotly.graph_objs as go

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
    "SRT3.DE": "Sa
