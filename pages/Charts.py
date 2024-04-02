import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.figure_factory as ff

data = pd.read_csv('IPL IMB381IPL2013.csv')

# get numeric columns
num_col = data.select_dtypes(include=np.number).columns.tolist()

# Unresolved issue: density plot not working with sold/base price
num_col.remove('BASE PRICE')
num_col.remove('SOLD PRICE')

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

# density chart append to chart list

if option in num_col:
    chart_list.append('Density Plot')

chart_op = st.multiselect('Select Chart(s) you want to see', chart_list,
                          key='chart_type', help="Density Plots will be shown for x-axis data")

st.subheader(f"Plot(s) of {option} and {option_2} for all players"
             f" indicating {option_col} by colour intensity.")

# Create plot

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
    if chart == 'Density Plot':
        fig = ff.create_distplot([data[option]], [option])
        st.plotly_chart(fig)


