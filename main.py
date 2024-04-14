import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn import linear_model
import statsmodels

decimal_points = 6

col = ["SOLD PRICE", "SIXERS", "AGE", "COUNTRY", "TEAM", "T-RUNS", "T-WKTS",
           "ODI-RUNS-S", "ODI-SR-B", "ODI-WKTS", "ODI-SR-BL", "CAPTAINCY EXP",
           "RUNS-S", "HS", "AVE", "SR-B", "RUNS-C", "WKTS",
           "AVE-BL", "ECON", "SR-BL", "AUCTION YEAR", "BASE PRICE"]

plyrRole = ['Allrounder', 'Batsman', 'Bowler', "W. Keeper"]

data = pd.read_csv('csv files/IPL IMB381IPL2013.csv')

st.title("Sold Price Analytics for IPL Player")

with st.expander("About this app 🏏"):
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

st.page_link("pages/charts.py",
             label="Click here to see Data Viz",
             icon="📈")

# Categories to show in dropdown menu

clmn1, clmn2 = st.columns(2)

with st.sidebar:

    option = st.selectbox("Select data used to predict", col,
                          key="main_op")

    col.remove(option)

    option_2 = st.selectbox("Select data to be predicted", col,
                            key="main_op_2")

    plyrRole_col = st.multiselect("Select playing role for which the player stats are to"
                                  " be aligned in regression and shown in the graph",
                                  plyrRole,
                                  key="regChart",
                                  default=plyrRole)

    if len(plyrRole_col) == 0:
        plyrRole_col = plyrRole
        st.info("If no playing role is selected, all the playing"
                " roles are taken for regression as default",
                icon="🧞")

with clmn1:
    # linear regression

    try:
        df_n = data[data['PLAYING ROLE'].isin(plyrRole_col)]
        indep_var = pd.DataFrame(df_n[option])
        dep_var = pd.DataFrame(df_n[option_2])

        lm = linear_model.LinearRegression()
        model = lm.fit(indep_var, dep_var)

        st.subheader(f"🧙 The linear regression of {option} and {option_2} for "
                     f"{', '.join(plyrRole_col)} playing role(s).")

        corr = df_n[option].corr(df_n[option_2])
        corr_fl = "{:.{}f}".format(corr, decimal_points)
        st.write(f'Correlation of {option} and {option_2} is : ' + str(corr_fl))

        coef_fl = "{:.{}f}".format(model.coef_[0][0], decimal_points)
        st.write(f"Slope : {str(coef_fl)}. In the context of cricket player data, the slope\n"
                 f" in a linear regression model represents the change in the\n"
                 f" dependent variable ({option_2}) for a one-unit \n"
                 f" change in the independent variable ({option})"
                 )

    except ValueError:
        st.info("Please select a playing role",
                icon="🙀")

with clmn2:
    try:
        coef_intercp = "{:.{}f}".format(model.intercept_[0], decimal_points)
        st.write("Intercept : " + str(coef_intercp) +
                 (" The intercept in a linear regression model is the predicted "
                  f"value of the dependent variable ({option_2}) when the \n"
                  f"independent variable ({option}) is zero"))

        rsq_fl = "{:.{}f}".format(model.score(indep_var, dep_var), decimal_points)
        st.write("R-Square value for the model : " + str(rsq_fl))

    except ValueError:
        st.info("Cannot find regression between the selected types "
                "of data",
                icon="😵")
    except NameError:
        st.info("Cannot find regression between the selected types "
                "of data",
                icon="🏏")

    try:
        indep_var_txt = st.text_input(f"Input {option} to predict {option_2} :",
                                      help="Enter appropriate values to get linear"
                                           " regression")
        indep_var_new = np.array([int(indep_var_txt)])
        indep_var_new = indep_var_new.reshape(-1, 1)
        dep_var_new = model.predict(indep_var_new)

        dep_var_n_fl = "{:.{}f}".format(dep_var_new[0][0], 3)
        st.info(f"The predicted value of {option_2} on the basis "
                f"of {option} is " + str(dep_var_n_fl))
        indep_var_int = int(indep_var_txt)
        X = ([indep_var_int / 2, indep_var_int * 2, indep_var_int * 5])
        X = pd.DataFrame(X)
        Y = model.predict(X)
        Y = pd.DataFrame(Y)
        df = pd.concat([X, Y], axis=1, keys=[option, f"{option_2} predicted"])
        st.write(df)

    except ValueError:
        st.info("Please enter a value in the box above or select appropriate"
                " data types to get linear regression",
                icon="🫠")
    except NameError:
        st.info("Please select numerical data to get linear regression",
                icon="⛈️")


with st.container():
    try:
        df_1 = data[data['PLAYING ROLE'].isin(plyrRole_col)]

        fig = px.scatter(df_1, x=option, y=option_2,
                         color='PLAYING ROLE', trendline="ols")
        st.plotly_chart(fig, use_container_width=True)
        fig_scat = px.scatter(df_1, x=option, y=option_2,
                              size="SOLD PRICE", color="PLAYING ROLE",
                              hover_name="COUNTRY", log_x=True, size_max=60
                              )
        st.plotly_chart(fig_scat, use_container_width=True)

    except ValueError:
        st.info("Please select appropriate data types to get the graph",
                icon="🚓")

# st.page_link("pages/player_list.py",
#             label="Click here to see the players list page along which"
#                   " the model is aligned",
#             icon="🏏")

disclaimer = "When you make conclusions from data analysis, you need" \
             " to make sure that you don’t assume a causal relationship" \
             " between elements of your data when there is only a correlation." \
             " When your data shows that outdoor temperature and ice cream" \
             " consumption both go up at the same time, it might be tempting" \
             " to conclude that hot weather causes people to eat ice cream." \
             " But, a closer examination of the data would reveal that every" \
             " change in temperature doesn’t lead to a change in ice cream" \
             " purchases. In addition, there might have been a sale on ice" \
             " cream at the same time that the data was collected, which" \
             " might not have been considered in your analysis"

with st.expander("Disclaimer"):
    st.warning(disclaimer)

