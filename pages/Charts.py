import streamlit as st
import pandas as pd
import plotly.express as px

data = pd.read_csv('IPL IMB381IPL2013.csv')

col_ch = ["COUNTRY", "TEAM", "PLAYING ROLE", "T-RUNS", "T-WKTS", "AGE",
       "ODI-RUNS-S", "ODI-SR-B", "ODI-WKTS", "ODI-SR-BL", "CAPTAINCY EXP",
       "RUNS-S", "HS", "AVE", "SR-B", "SIXERS", "RUNS-C", "WKTS",
       "AVE-BL", "ECON", "SR-BL", "AUCTION YEAR", "BASE PRICE", "SOLD PRICE"]

chart_list = ['Bar', 'Scatter', 'Plotly']

option = st.selectbox("Select data to view on x-axis", col_ch,
                      key='chart_op')

pop_var = col_ch.index(option)

col_ch.pop(pop_var)

option_2 = st.selectbox("Select data to view on y-axis", col_ch,
                        key='chart_op_2')

pop_var = col_ch.index(option_2)

col_ch.pop(pop_var)

option_col = st.selectbox("Select data to to be shown by its colour intensity in the graph", col_ch,
                          key='chart_op_col')

chart_op = st.multiselect('Select Chart(s) you want to see', chart_list,
                          key='chart_type')

st.subheader(f"Here is/are plot(s) of {option} and {option_2} for all players"
             f" grouped by {option_col}.")

# Create a plot

for chart in chart_op:
    if chart == 'Bar':
        st.bar_chart(data, x=option, y=option_2, color=option_col)
    if chart == 'Scatter':
        st.scatter_chart(data, x=option, y=option_2, color=option_col)
    if chart == 'Plotly':
        fig = px.scatter(data, x=option, y=option_2, color=option_col)
        st.plotly_chart(fig)
        fig_2 = px.bar(data, x=option, y=option_2, color=option_col)
        st.plotly_chart(fig_2)
