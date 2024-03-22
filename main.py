import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn import linear_model
import numpy as np

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

# linear regression

try:
    st.subheader(f"Here is the linear regression of {option} and {option_2} for all players.")
    corr = data[option].corr(data[option_2])
    st.write(corr)

    indep_var = pd.DataFrame(data[option])
    dep_var = pd.DataFrame(data[option_2])

    lm = linear_model.LinearRegression()
    model = lm.fit(indep_var, dep_var)

    st.write("Slope : {0}".format(str(model.coef_)))

    st.write("Intercept : " + str(model.intercept_))

    st.write("R-Square value for the model : " + str(model.score(indep_var, dep_var)))

    indep_var_txt = st.text_input(f"Input {option} to predict {option_2} :")
    indep_var_new = np.array([int(indep_var_txt)])
    indep_var_new = indep_var_new.reshape(-1, 1)
    dep_var_new = model.predict(indep_var_new)
    st.write(dep_var_new)

    indep_var_int = int(indep_var_txt)
    X = ([indep_var_int / 2, indep_var_int * 2, indep_var_int * 5])
    X = pd.DataFrame(X)
    Y = model.predict(X)
    Y = pd.DataFrame(Y)
    df = pd.concat([X,Y],axis=1, keys = [option, f"{option_2} predicted"])
    st.write(df)

except ValueError:
    st.info("Cannot find regression between the selected values")

filtered_data = data[['PLAYER NAME', option, option_2]]

if player:
    # Get the player data
    player_role = data.loc[data['PLAYER NAME'] == player, 'PLAYING ROLE'].values[0]
    player_value = filtered_data.loc[filtered_data['PLAYER NAME'] == player, (option, option_2)].values[0]
    st.info(f"{player} is a {player_role} whose {option} is/are {player_value[0]} " +
             f"and the {option_2} is/are {player_value[1]}.")

st.subheader(f"Here is scatter plot of {option} and {option_2} for all players.")

# Create a plot

fig = px.scatter(data, x=option, y=option_2, color="PLAYING ROLE")
st.plotly_chart(fig)

fig_2 = px.bar(data, x=option, y=option_2, color='PLAYING ROLE')
st.plotly_chart(fig_2)
