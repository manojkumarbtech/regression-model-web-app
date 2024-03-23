import pandas as pd
import streamlit as st
from sklearn import linear_model
import numpy as np

data = pd.read_csv('IPL IMB381IPL2013.csv')

st.title("Sold Price Estimate for IPL Player")

st.page_link("pages/Player_List.py",
             label="Check the player list page to"
                   " get player names.",
             icon="🏏")

st.page_link("pages/Charts.py",
             label="Click here to see Data Viz",
             icon="📈")

# Categories to show in dropdown menu

col = ("SOLD PRICE", "AGE", "COUNTRY", "TEAM", "T-RUNS", "T-WKTS",
       "ODI-RUNS-S", "ODI-SR-B", "ODI-WKTS", "ODI-SR-BL", "CAPTAINCY EXP",
       "RUNS-S", "HS", "AVE", "SR-B", "SIXERS", "RUNS-C", "WKTS",
       "AVE-BL", "ECON", "SR-BL", "AUCTION YEAR", "BASE PRICE")

option = st.selectbox("Select data used to predict (view on horizontal axis)", col,
                      key="main_op")

option_2 = st.selectbox("Select data to be predicted (view on vertical axis)", col,
                        key="main_op_2")

# linear regression

try:
    st.subheader(f"Here is the linear regression of {option} and {option_2} for all players."
                 , help="Enter appropriate values to get linear regression"
                 )
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
    st.info(dep_var_new[0][0])

    indep_var_int = int(indep_var_txt)
    X = ([indep_var_int / 2, indep_var_int * 2, indep_var_int * 5])
    X = pd.DataFrame(X)
    Y = model.predict(X)
    Y = pd.DataFrame(Y)
    df = pd.concat([X,Y],axis=1, keys = [option, f"{option_2} predicted"])
    st.write(df)

except ValueError:
    st.info("Cannot find regression between the selected values")
