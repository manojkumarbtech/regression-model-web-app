import streamlit as st
import pandas as pd

data_1 = pd.read_csv('IPL IMB381IPL2013.csv')

num_play = st.slider("What is the range of players you want to get details of ?", value=(1, 130),
                     help="SSSSSSSSLLLLLIIIIIDDDDDEEEEE")
num_col = st.slider("What is the range of columns you want to see?", value=(1, 26),
                     help="Total Columns = 26")

col = ["Sl.NO.", "PLAYER NAME", "AGE", "COUNTRY", "TEAM", "PLAYING ROLE",
       "T-RUNS", "T-WKTS", "ODI-RUNS-S", "ODI-SR-B", "ODI-WKTS", "ODI-SR-BL",
       "CAPTAINCY EXP", "RUNS-S", "HS", "AVE", "SR-B", "SIXERS", "RUNS-C", "WKTS",
       "AVE-BL", "ECON", "SR-BL", "AUCTION YEAR", "BASE PRICE",
       "SOLD PRICE"
       ]

disp_col = col[num_col[0]:num_col[1]]

st.write(data_1[disp_col][num_play[0]:num_play[1]])
