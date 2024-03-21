import pandas as pd
import plotly.express as px
import streamlit as st

prompt = "Enter Player (use the format: <surname>, <firstname" \
         " initials> for e.g. Dilshan, TM): "

data = pd.read_csv('IPL IMB381IPL2013.csv')

sold_price = 0

st.title("Sold Price Estimate for IPL Player")
player = st.text_input(prompt)

days = st.slider("Look at this slider", min_value=1, max_value=5,
                 help="SSSSSSSSLLLLLIIIIIDDDDDEEEEE")

col = ("SOLD PRICE", "AGE", "COUNTRY", "TEAM", "T-RUNS", "T-WKTS",
       "ODI-RUNS-S", "ODI-SR-B", "ODI-WKTS", "ODI-SR-BL", "CAPTAINCY EXP",
       "RUNS-S", "HS", "AVE", "SR-B", "SIXERS", "RUNS-C", "WKTS",
       "AVE-BL", "ECON", "SR-BL", "AUCTION YEAR", "BASE PRICE")

option = st.selectbox("Select data to view on x-axis", col)

option_2 = st.selectbox("Select data to view on y-axis", col)

if player:
    # Get the player data
    player_role = data.loc[data['PLAYER NAME'] == player, 'PLAYING ROLE'].values[0]
    filtered_data = data[['PLAYER NAME', option, option_2]]
    player_value = filtered_data.loc[filtered_data['PLAYER NAME'] == player, (option, option_2)].values[0]
    st.write(f"{player_role}'s {option} is/are {player_value[0]}.")
    st.write(f"And the {option_2} is/are {player_value[1]}.")

st.subheader(f"Here is scatter plot of {option} and {option_2} for all players.")

# Create a plot

fig = px.scatter(data, x=option, y=option_2, color="PLAYING ROLE")
st.plotly_chart(fig)

st.subheader(f"Here is the correlation of {option} and {option_2} for all players.")

try:
    st.write(data[option].corr(data[option_2]))
except ValueError:
    st.write("Cannot find correlation between the selected values")

fig_2 = px.bar(data, x=option, y=option_2, color='PLAYING ROLE')
st.plotly_chart(fig_2)
