import streamlit as st
import pandas as pd

data = pd.read_csv('IPL IMB381IPL2013.csv')

col = ("COUNTRY", "TEAM", "T-RUNS", "T-WKTS", "AGE",
       "ODI-RUNS-S", "ODI-SR-B", "ODI-WKTS", "ODI-SR-BL", "CAPTAINCY EXP",
       "RUNS-S", "HS", "AVE", "SR-B", "SIXERS", "RUNS-C", "WKTS",
       "AVE-BL", "ECON", "SR-BL", "AUCTION YEAR", "BASE PRICE", "SOLD PRICE")

option = st.selectbox("Select data to view on x-axis", col)

option_2 = st.selectbox("Select data to view on y-axis", col)

st.bar_chart(data, x=option, y=option_2, color='COUNTRY')
