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

    # This concatenation will produce the actual total dataframe with unique entries for each player because of groupby
    df_all = pd.concat(df_list).groupby(['Player']).sum().reset_index()

    # We merge the season count into the total dataframe to add the Season column
    df_all_with_season_count = df_all.merge(df_season_count, on='Player', how='left')

    return df_all_with_season_count


def formatBattingCombined(df_batting_combined):
    # Will divide average and Strike Rate by number of seasons to get the average of these metrics across all seasons
    df_batting_combined['Avg'] = round(df_batting_combined['Avg'] / df_batting_combined['Seasons'], 2)
    df_batting_combined['SR'] = round(df_batting_combined['SR'] / df_batting_combined['Seasons'], 2)

    return df_batting_combined


batting_file_path = "cleaned_datasets/Batting Stats"

bowling_file_path = "cleaned_datasets/Bowling Stats"


# All batting dataframes
df_batting_2016 = load_data(batting_file_path, "batting_data_2016.csv")
df_batting_2017 = load_data(batting_file_path, "batting_data_2017.csv")
df_batting_2018 = load_data(batting_file_path, "batting_data_2018.csv")
df_batting_2019 = load_data(batting_file_path, "batting_data_2019.csv")
df_batting_2020 = load_data(batting_file_path, "batting_data_2020.csv")
df_batting_2021 = load_data(batting_file_path, "batting_data_2021.csv")
df_batting_2022 = load_data(batting_file_path, "batting_data_2022.csv")

batting_list = [df_batting_2016,
                df_batting_2017,
                df_batting_2018,
                df_batting_2019,
                df_batting_2020,
                df_batting_2021,
                df_batting_2022
                ]

filtered_batting_list = []

# All bowling dataframes
df_bowling_2016 = load_data(bowling_file_path, "bowling_data_2016.csv")
df_bowling_2017 = load_data(bowling_file_path, "bowling_data_2017.csv")
df_bowling_2018 = load_data(bowling_file_path, "bowling_data_2018.csv")
df_bowling_2019 = load_data(bowling_file_path, "bowling_data_2019.csv")
df_bowling_2020 = load_data(bowling_file_path, "bowling_data_2020.csv")
df_bowling_2021 = load_data(bowling_file_path, "bowling_data_2021.csv")
df_bowling_2022 = load_data(bowling_file_path, "bowling_data_2022.csv")


yr_list = st.slider("Select the years you want the data for",
                    value=(2016, 2022),
                    min_value=2016,
                    max_value=2022)

col1, col2 = st.columns(2)

for yr in range(yr_list[0], yr_list[1] + 1):
    filtered_batting_list.append(load_data(batting_file_path,
                                           f"batting_data_{str(yr)}.csv"))

df_1 = combine_df_season_cnt(filtered_batting_list)
st.write(df_1)

