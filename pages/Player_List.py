import streamlit as st
import pandas as pd

data_1 = pd.read_csv('IPL IMB381IPL2013.csv')

num_play = st.slider("What is the range of players you want to get details of ?", value=(1, 130),
                     help="SSSSSSSSLLLLLIIIIIDDDDDEEEEE")

st.write(data_1[['PLAYER NAME', 'PLAYING ROLE', 'AGE', 'COUNTRY', 'TEAM', 'BASE PRICE', 'SOLD PRICE', "AUCTION YEAR"]][
         num_play[0]:num_play[1]])
