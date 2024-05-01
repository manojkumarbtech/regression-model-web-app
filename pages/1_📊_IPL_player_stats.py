import os
import pandas as pd
import warnings
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

warnings.filterwarnings("ignore")


def load_data(file_path, filename):
    csv_path = os.path.join(file_path, filename)
    return pd.read_csv(csv_path)


def combine_df_season_cnt(df_list):

    # This is used to concatenate the dataframes and count the number of
    # seasons each player played by counting the duplicates
    df_season_count = pd.concat(df_list)["Player"].value_counts().reset_index()

    # We will rename the columns for this dataframe to easily merge into the total dataframe
    df_season_count = df_season_count.rename(columns={"count": "Seasons"})

    # This concatenation will produce the actual total dataframe with unique
    # entries for each player because of groupby
    df_max = pd.concat(df_list).groupby(['Player']).max().reset_index()

    df_all = pd.concat(df_list).groupby(['Player']).sum().reset_index()

    # We merge the season count into the total dataframe to add the Season column
    df_all_with_season_count = df_all.merge(df_season_count, on='Player', how='left')

    return df_all_with_season_count, df_max


def formatBattingCombined(df_batting_combined, df_batting_max):
    # Will divide average and Strike Rate by number of seasons to get the average of these metrics across all seasons

    df_batting_combined['Avg'] = round(df_batting_combined['Runs'] / df_batting_combined['Inns'], 2)
    df_batting_combined['SR'] = round(df_batting_combined['Runs'] / df_batting_combined['BF'] * 100, 2)
    df_batting_combined['POS'] = round(df_batting_combined['POS'] / df_batting_combined['Seasons'], 2)
    df_batting_combined['HS'] = df_batting_max['HS']

    return df_batting_combined


# stats_op = st.selectbox(f"Select the stats you want to see",
#                         ('Batting Stats', 'Bowling Stats'), key='stats_op')

batting_file_path = "cleaned_datasets/Batting Stats"

# bowling_file_path = "cleaned_datasets/Bowling Stats"

filtered_batting_list = []

# Insert page header here

yr_list = st.slider("Select the years you want the data for",
                    value=(2016, 2022),
                    min_value=2016,
                    max_value=2022)

for yr in range(yr_list[0], yr_list[1] + 1):
    filtered_batting_list.append(load_data(batting_file_path,
                                           f"batting_data_{str(yr)}.csv"))

df_1, df_2 = combine_df_season_cnt(filtered_batting_list)

df_3 = formatBattingCombined(df_1, df_2)

# st.write(df_3)

st.subheader(f"📉 5 Batsmen with highest T20 Runs in the period {yr_list[0]}-{yr_list[1]}")

df_most_runs = df_3.sort_values(by=['Runs'], ascending=False)[:5].copy()
plt.figure(figsize=(20, 10))
plt.title(f"5 Batsmen with highest T20 Runs in the period {yr_list[0]}-{yr_list[1]}")
ax = sns.barplot(x=df_most_runs["Runs"], y=df_most_runs["Player"], palette="husl")
ax.set(ylabel="Player Name", xlabel="Runs Scored")
st.pyplot(fig=plt)
