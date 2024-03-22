import pandas as pd
import plotly.express as px
import streamlit as st

prompt = " Enter player by using the format: <surname>, <firstname" \
         " initials> for e.g. Dilshan, TM :"

data = pd.read_csv('IPL IMB381IPL2013.csv')

sold_price = 0

st.title("Sold Price Estimate for IPL Player")
player = st.text_input(prompt)

st.page_link("pages/Player_List.py",
             label="Check the player list page to"
                   " get player names.",
             icon="🏏")

# Categories to show in dropdown menu

col = ("SOLD PRICE", "AGE", "COUNTRY", "TEAM", "T-RUNS", "T-WKTS",
       "ODI-RUNS-S", "ODI-SR-B", "ODI-WKTS", "ODI-SR-BL", "CAPTAINCY EXP",
       "RUNS-S", "HS", "AVE", "SR-B", "SIXERS", "RUNS-C", "WKTS",
       "AVE-BL", "ECON", "SR-BL", "AUCTION YEAR", "BASE PRICE")

option = st.selectbox("Select data to view on x-axis and for the specific player", col)

option_2 = st.selectbox("Select data to view on y-axis and for the specific player", col)

filtered_data = data[['PLAYER NAME', option, option_2]]

if player:
    # Get the player data
    player_role = data.loc[data['PLAYER NAME'] == player, 'PLAYING ROLE'].values[0]
    player_value = filtered_data.loc[filtered_data['PLAYER NAME'] == player, (option, option_2)].values[0]
    st.write(f"{player} is a {player_role} whose {option} is/are {player_value[0]} " +
             f"and the {option_2} is/are {player_value[1]}.")

st.subheader(f"Here is scatter plot of {option} and {option_2} for all players.")

# Create a plot

fig = px.scatter(data, x=option, y=option_2, color="PLAYING ROLE")
st.plotly_chart(fig)

# Correlation for two categories

try:
    st.subheader(f"Here is the correlation of {option} and {option_2} for all players.")
    st.write(data[option].corr(data[option_2]))
except ValueError:
    st.write("Cannot find correlation between the selected values")

fig_2 = px.bar(data, x=option, y=option_2, color='PLAYING ROLE')
st.plotly_chart(fig_2)
