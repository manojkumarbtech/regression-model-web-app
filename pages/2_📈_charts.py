import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import altair as alt

data_unf = pd.read_csv('csv files/IPL IMB381IPL2013.csv')

# st.title('Data Visualization of IPL players')

chart_list = ['Bar', 'Scatter', 'Plotly', 'Plotly-2',
              'Histogram', 'Distribution Plot']

# get numeric columns
num_col = data_unf.select_dtypes(include=np.number).columns.tolist()

# Unresolved issue: density plot not working with big numbers
num_col.remove('BASE PRICE')
num_col.remove('SOLD PRICE')
num_col.remove('ODI-RUNS-S')
num_col.remove('T-RUNS')

col_ch = ["COUNTRY", "ODI-RUNS-S", "ODI-SR-B", "T-WKTS", "AGE", "ODI-WKTS",
          "TEAM", "PLAYING ROLE", "T-RUNS", "ODI-SR-BL", "CAPTAINCY EXP",
          "RUNS-S", "HS", "AVE", "SR-B", "SIXERS", "RUNS-C", "WKTS",
          "AVE-BL", "ECON", "SR-BL", "AUCTION YEAR", "BASE PRICE", "SOLD PRICE"]

plyrRole = ['Allrounder', 'Batsman', 'Bowler', "W. Keeper"]

plyrRole_col = st.multiselect("Select playing role by which the player stats are to"
                              " be shown in the graph(s)",
                              plyrRole,
                              default=plyrRole,
                              key="rolChart")

with st.sidebar:

    try:
        data = data_unf[data_unf['PLAYING ROLE'].isin(plyrRole_col)]
    except NameError:
        st.info("Sorry, something went wrong",
                icon="🫠")

    option = st.selectbox("Select data to view on x-axis", col_ch,
                          key='chart_op')

    # define a list to store df on the basis of plyr role and option to be used in
    # dist plot

    dfs = []

    for rol in plyrRole_col:
        dfs.append(data_unf[data_unf['PLAYING ROLE'] == rol][option])

    col_ch.remove(option)

    option_2 = st.selectbox("Select data to view on y-axis", col_ch,
                            key='chart_op_2')

    col_ch.remove(option_2)

    option_col = st.selectbox("Select data to to be shown by its colour intensity in the graph", col_ch,
                              key='chart_op_col')

st.write(f"Plots of {option} and {option_2}"
         f" indicating {option_col} by colour intensity for "
         f"{', '.join(plyrRole_col)} playing role(s). Histogram and "
         f" Distribution plots are shown for x-axis data. ")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(chart_list)

# Create plot

with tab1:

    st.bar_chart(data, x=option, y=option_2,
                 color=option_col,
                 use_container_width=True)

with tab2:

    st.scatter_chart(data, x=option, y=option_2,
                     color=option_col,
                     use_container_width=True)

with tab3:

    fig = px.scatter(data, x=option, y=option_2,
                     color=option_col)
    st.plotly_chart(fig, use_container_width=True)

with tab4:

    fig_2 = px.bar(data, x=option, y=option_2,
                   color=option_col)
    st.plotly_chart(fig_2, use_container_width=True)

with tab5:

    fig = px.histogram(data[data['PLAYING ROLE'].isin(plyrRole_col)],
                       x=option,
                       color='PLAYING ROLE')
    st.plotly_chart(fig, use_container_width=True)

with tab6:

    if option in num_col:
        fig_ff = ff.create_distplot(dfs,
                                    group_labels=plyrRole_col)

        st.plotly_chart(fig_ff, use_container_width=True)

    # chart not ready
    # if chart == 'Altair':
    #     c = (
    #         alt.Chart(data)
    #         .mark_circle()
    #          .encode(x=option, y=option_2, size='SOLD PRICE',
    #                color=option_col,
    #                tooltip=["SOLD PRICE", "PLAYING ROLE"])
    #     )

    #     st.altair_chart(c, use_container_width=True)
