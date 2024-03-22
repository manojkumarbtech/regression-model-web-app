import streamlit as st
import pandas as pd

prompt = " Enter player by using the format: <surname>, <firstname" \
         " initials> for e.g. Dilshan, TM :"

data_1 = pd.read_csv('IPL IMB381IPL2013.csv')

col = ["Sl.NO.", "PLAYER NAME", "AGE", "COUNTRY", "TEAM", "PLAYING ROLE",
       "T-RUNS", "T-WKTS", "ODI-RUNS-S", "ODI-SR-B", "ODI-WKTS", "ODI-SR-BL",
       "CAPTAINCY EXP", "RUNS-S", "HS", "AVE", "SR-B", "SIXERS", "RUNS-C", "WKTS",
       "AVE-BL", "ECON", "SR-BL", "AUCTION YEAR", "BASE PRICE",
       "SOLD PRICE"
       ]

option = st.selectbox("Select data to view for the specific player", col)

option_2 = st.selectbox("Select data to view for the specific player", col)

filtered_data = data_1[['PLAYER NAME', option, option_2]]

player = st.text_input(prompt)

if player:
    # Get the player data
    player_role = data_1.loc[data_1['PLAYER NAME'] == player, 'PLAYING ROLE'].values[0]
    player_value = filtered_data.loc[filtered_data['PLAYER NAME'] == player, (option, option_2)].values[0]
    st.info(f"{player} is a {player_role} whose {option} is/are {player_value[0]} " +
            f"and the {option_2} is/are {player_value[1]}.")

num_play = st.slider("What is the range of players you want to get details of ?", value=(1, 130),
                     help="SSSSSSSSLLLLLIIIIIDDDDDEEEEE")
num_col = st.slider("What is the range of columns you want to see?", value=(1, 26),
                     help="Total Columns = 26")

disp_col = col[num_col[0]:num_col[1]]

st.write(data_1[disp_col][num_play[0]:num_play[1]])
