import pandas as pd
import streamlit as st
from sklearn import linear_model
import numpy as np

data = pd.read_csv('IPL IMB381IPL2013.csv')

st.title("Sold Price Estimate for IPL Player")

with st.expander("About this app"):
    st.write("""
        Get in the IPL spirit this season by playing around with
        this fun app! Predict any feature for e.g. the number of sixers
        a player may hit using their base or sold price.
        """)
    st.info("""
        Linear regression is a statistical method used to understand the
         relationship between two variables by fitting a linear equation
          to the observed data
        """)

st.page_link("pages/Player_List.py",
             label="Click here to see the players list page",
             icon="🏏")

st.page_link("pages/Charts.py",
             label="Click here to see Data Viz",
             icon="📈")

# Categories to show in dropdown menu

col = ("SOLD PRICE", "AGE", "COUNTRY", "TEAM", "T-RUNS", "T-WKTS",
       "ODI-RUNS-S", "ODI-SR-B", "ODI-WKTS", "ODI-SR-BL", "CAPTAINCY EXP",
       "RUNS-S", "HS", "AVE", "SR-B", "SIXERS", "RUNS-C", "WKTS",
       "AVE-BL", "ECON", "SR-BL", "AUCTION YEAR", "BASE PRICE")

option = st.selectbox("Select data used to predict", col,
                      key="main_op")

option_2 = st.selectbox("Select data to be predicted", col,
                        key="main_op_2")

# linear regression

try:
    st.subheader(f"Here is the linear regression of {option} and {option_2} for all players."
                 , help="Enter appropriate values to get linear regression"
                 )
    corr = data[option].corr(data[option_2])
    st.write(f'Correlation of {option} and {option_2} is : ' + str(corr))

    indep_var = pd.DataFrame(data[option])
    dep_var = pd.DataFrame(data[option_2])

    lm = linear_model.LinearRegression()
    model = lm.fit(indep_var, dep_var)

    st.write(f"Slope : {str(model.coef_[0][0])}. In the context of cricket player data, the slope\n"
             f" in a linear regression model represents the change in the\n"
             f" dependent variable ({option_2}) for a one-unit \n"
             f" change in the independent variable ({option})"
             )

    st.write("Intercept : " + str(model.intercept_[0]) +
             (" The intercept in a linear regression model is the predicted "
              "value of the dependent variable when the \n"
              "independent variable is zero"))

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
    df = pd.concat([X, Y], axis=1, keys=[option, f"{option_2} predicted"])
    st.write(df)

except ValueError:
    st.info("Cannot find regression between the selected values")
