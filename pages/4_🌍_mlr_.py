import streamlit as st

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
    st.write(disclaimer)
