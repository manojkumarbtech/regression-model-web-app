import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Multiple linear regression (Beta)")

prompt = 'Select a categorical i.e. non-numeric data.'

data = pd.read_csv('csv files/IPL IMB381IPL2013.csv')

col_mlr = ["COUNTRY", "TEAM", "PLAYING ROLE", "AGE",
       "CAPTAINCY EXP", "AUCTION YEAR"]

col_num = ["T-RUNS", "T-WKTS", "AGE", "ODI-RUNS-S", "ODI-SR-B", "ODI-WKTS", "ODI-SR-BL",
           "CAPTAINCY EXP", "RUNS-S", "HS", "AVE", "SR-B", "SIXERS", "RUNS-C", "WKTS",
           "AVE-BL", "ECON", "SR-BL", "AUCTION YEAR", "BASE PRICE", "SOLD PRICE"]

with st.sidebar:
    heatmap_op_1 = st.selectbox('Select Features you want to see on horizonatal axis of the heatmap', col_mlr,
                                key='heatmap_x', help=prompt)

    pop_var = col_mlr.index(heatmap_op_1)

    col_mlr.pop(pop_var)

    heatmap_op_2 = st.selectbox('Select Features you want to see on vertical axis of the heatmap', col_mlr,
                                key='heatmap_y', help=prompt)

    heatmap_op_num = st.selectbox('Select data to to be shown by its colour intensity in the heatmap', col_num,
                                  key='heatmap_z')

try:
    df = data.pivot_table(index=heatmap_op_2, columns=heatmap_op_1, values=heatmap_op_num)
    fig = px.imshow(df)
    st.plotly_chart(fig)

except ValueError:
    st.warning("Select distinct data on horizontal & vertical axes and the color intensity")

# with st.expander("Don`t click here!"):
#     st.write("Stats-for-nerds")
#     st.info(st.session_state)
