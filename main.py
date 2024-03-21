import pandas as pd
import plotly.express as px
import streamlit as st

data = pd.read_csv('IPL IMB381IPL2013.csv')

sold_price = 0

st.title("Sold Price Estimate for IPL Player")
player = st.text_input("Enter Player (use the format: <surname>, <firstname"
                       " initials> for e.g. Dilshan, TM): ")

days = st.slider("Look at this slider", min_value=1, max_value=5,
                 help="SSSSSSSSLLLLLIIIIIDDDDDEEEEE")

option = st.selectbox("Select data to view on x-axis",
                      ("SOLD PRICE", "AGE", "COUNTRY", "TEAM", "PLAYING ROLE",
                       "T-RUNS", "T-WKTS", "ODI-RUNS-S", "ODI-SR-B", "ODI-WKTS",
                       "ODI-SR-BL", "CAPTAINCY EXP", "RUNS-S", "HS", "AVE",
                       "SR-B", "SIXERS", "RUNS-C", "WKTS", "AVE-BL", "ECON",
                       "SR-BL", "AUCTION YEAR", "BASE PRICE"))

option_2 = st.selectbox("Select data to view on y-axis",
                        ("SOLD PRICE", "AGE", "COUNTRY", "TEAM", "PLAYING ROLE",
                         "T-RUNS", "T-WKTS", "ODI-RUNS-S", "ODI-SR-B", "ODI-WKTS",
                         "ODI-SR-BL", "CAPTAINCY EXP", "RUNS-S", "HS", "AVE",
                         "SR-B", "SIXERS", "RUNS-C", "WKTS", "AVE-BL", "ECON",
                         "SR-BL", "AUCTION YEAR", "BASE PRICE"))

if player:
    # Get the player data
    player_role = data.loc[data['PLAYER NAME'] == player, 'PLAYING ROLE'].values[0]
    filtered_data = data[['PLAYER NAME', option, option_2]]
    player_value = filtered_data.loc[filtered_data['PLAYER NAME'] == player, (option, option_2)].values[0]
    st.write(f"{player_role}'s {option} is/are {player_value[0]}.")
    st.write(f"And the {option_2} is/are {player_value[1]}.")

st.subheader(f"Here is scatter plot of {option} and {option_2} for all players.")

# Create a plot
figure = px.scatter(x=data[option], y=data[option_2], labels={"x": option, "y": option_2})
st.plotly_chart(figure)

st.subheader(f"Here is the correlation of {option} and {option_2} for all players.")

st.write(data[option].corr(data[option_2]))
