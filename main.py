import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn import linear_model
import statsmodels

decimal_points = 6

# heat-map prompt

help_prompt = ('Data used to predict will be shown by'
               ' its colour intensity in the heatmap')

# Categories to show in dropdown menu

col = ["SOLD PRICE", "SIXERS", "AGE", "T-RUNS", "T-WKTS",
       "ODI-RUNS-S", "ODI-SR-B", "ODI-WKTS", "ODI-SR-BL", "CAPTAINCY EXP",
       "RUNS-S", "HS", "AVE", "SR-B", "RUNS-C", "WKTS",
       "AVE-BL", "ECON", "SR-BL", "AUCTION YEAR", "BASE PRICE"]

plyrRole = ['Allrounder', 'Batsman', 'Bowler', "W. Keeper"]

col_mlr = ["COUNTRY", "TEAM", "PLAYING ROLE", "AGE",
           "CAPTAINCY EXP", "AUCTION YEAR"]

data = pd.read_csv('csv files/IPL IMB381IPL2013.csv')

st.title("Auction Price Analytics for IPL Player")

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

with st.sidebar:
    option = st.selectbox("Select data used to predict", col,
                          key="main_op")

    col.remove(option)

    option_2 = st.selectbox("Select data to be predicted", col,
                            key="main_op_2")

    heatmap_op = st.multiselect('Select features you want to see on the heatmap',
                                col_mlr,
                                key='heatmap',
                                help=help_prompt,
                                default=['PLAYING ROLE', 'TEAM'])

    st.write("""
            🏏 Get in the IPL spirit this season by playing around with
            this fun app! Predict any feature for e.g. the number of sixers
            a player may hit using their base or auction price.
            """)

try:
    df_n = data[data['PLAYING ROLE'].isin(plyrRole_col)]
    indep_var = pd.DataFrame(df_n[option])
    dep_var = pd.DataFrame(df_n[option_2])

    lm = linear_model.LinearRegression()
    model = lm.fit(indep_var, dep_var)

    optionLow = option.lower()
    option2Low = option_2.lower()

    st.subheader(f"📈 The linear regression of {optionLow} and {option2Low} for "
                 f"{', '.join(plyrRole_col)} playing role(s).")

except ValueError:
    st.info("Cannot find regression between the selected types "
            "of data",
            icon="🙀")

tab1, tab2, tab3 = st.tabs(["Trendline Graph", "Bubble Graph", "Heat-Map Graph"])

with tab1:
    df_1 = data[data['PLAYING ROLE'].isin(plyrRole_col)]

    fig = px.scatter(df_1, x=option, y=option_2,
                     color='PLAYING ROLE', trendline="ols")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig_scat = px.scatter(df_1, x=option, y=option_2,
                          size="SOLD PRICE", color="PLAYING ROLE",
                          hover_name="COUNTRY", log_x=True, size_max=60
                          )
    st.plotly_chart(fig_scat, use_container_width=True)

with tab3:

    if len(heatmap_op) < 2:
        heatmap_op = ['PLAYING ROLE', 'TEAM']

    try:
        df = data.pivot_table(index=heatmap_op[0],
                              columns=heatmap_op[1],
                              values=option)

        fig = px.imshow(df)

        st.plotly_chart(fig,
                        use_container_width=True)

    except ValueError:
        st.warning("Select distinct data for horizontal,"
                   " vertical axes and the color intensity",
                   icon="⛈️")

st.info("Linear regression is a statistical method used to understand the"
        "relationship between two variables by fitting a linear equation"
        "to the observed data")

clmn1, clmn2 = st.columns(2)

with clmn1:

    # linear regression
    try:
        indep_var_txt = st.text_input(f"Input {optionLow} to predict {option2Low} :",
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
        st.info("Please enter a value in the box above to get linear regression",
                icon="🫠")

with clmn2:

    try:
        corr = df_n[option].corr(df_n[option_2])
        corr_fl = "{:.{}f}".format(corr, decimal_points)

        with st.popover(label=f"Correlation : {str(corr_fl)}",
                        use_container_width=True):
            st.write(f'Correlation reflects how similar the values of'
                     f' two or more variables are across a dataset')

        coef_fl = "{:.{}f}".format(model.coef_.squeeze(), decimal_points)
        coef_intercp = "{:.{}f}".format(model.intercept_[0], decimal_points)
        rsq_fl = "{:.{}f}".format(model.score(indep_var, dep_var), decimal_points)

        with st.popover(label=f"Slope : {str(coef_fl)}",
                        use_container_width=True):
            st.write(f"In the context of cricket player data, the slope\n"
                     f" in a linear regression model represents the change in the\n"
                     f" dependent variable ({option_2}) for a one-unit \n"
                     f" change in the independent variable ({option})"
                     )

        with st.popover(label=f"Intercept : {str(coef_intercp)}",
                        use_container_width=True):
            st.write(" The intercept in a linear regression model is the predicted "
                     f"value of the dependent variable ({option_2}) when the \n"
                     f"independent variable ({option}) is zero")

        with st.popover(label=f'R-Square : {str(rsq_fl)}',
                        use_container_width=True):
            st.write("R-Square value for the model "
                     "indicates the percentage of the variance in the dependent variable "
                     "that the independent variable explains.")

    except ValueError:
        st.info("Cannot find regression between the selected types "
                "of data",
                icon="😵")
    except NameError:
        st.info("Cannot find regression between the selected types "
                "of data",
                icon="🏏")

# st.page_link("pages/2_📈_charts.py",
#             label="Click here to see Data Viz",
#             icon="🧙")

# st.page_link("pages/3_🏏_player_list.py",
#             label="Click here to see the players list page along which"
#                   " the model is aligned",
#             icon="🏏")

