import streamlit as st
import pandas as pd

prompt_1 = "Enter player name for e.g. Jasprit Bumrah"

filepath_player_auc = 'csv files/IPL_2023-22_Sold_Players.csv'

# define default player
player_def = "Virat Kohli"

with st.sidebar:
    player = st.text_input(label=prompt_1, value=player_def)

    stats_op = st.selectbox(f"Select the stats you want to see of {player}",
                            ('Batting Stats', 'Bowling Stats'), key='stats_op')

# define select-box items
col_pl = []
col_pl_temp = []

# define filepath for player stats
filepath_cric = ""

try:
    # load player role and auction data
    data_1 = pd.read_csv(filepath_player_auc)
except FileNotFoundError:
    st.warning("Woah there! pardner")

filtered_data = data_1[['AUCTION YEAR', 'Name', 'Type', 'Price']]

if player:
    # Get the player data
    try:
        player_role = filtered_data.loc[filtered_data['Name'].str.strip() == player, 'Type'].values[0]
        player_auc_price = filtered_data.loc[filtered_data['Name'].str.strip() == player, 'Price'].values[0]
        st.info(player + f"`s auction price was INR {player_auc_price}.")

    except IndexError:
        st.info(player + " might not have been auctioned.")
        player_role = 'player'

    if 'Batting Stats' == stats_op:
        # display batting stats of the player
        col_pl = ["POS", "Player", "Mat", "Inns", "NO", "Runs",
                  "HS", "Avg", "BF", "SR", "100", "50", "4s", "6s"
                  ]
        col_pl_temp = ["POS", "Player", "Mat", "Inns", "NO", "Runs",
                       "HS", "Avg", "BF", "SR", "100", "50", "4s", "6s"
                       ]

        filepath_cric = "csv files/BATTING STATS - IPL_2022.csv"

    if 'Bowling Stats' == stats_op:
        # display bowling stats of the player
        col_pl = ["POS", "Player", "Mat", "Inns", "Ov", "Runs", "Wkts",
                  "BBI", "Avg", "Econ", "SR", "4w", "5w"
                  ]

        col_pl_temp = ["POS", "Player", "Mat", "Inns", "Ov", "Runs", "Wkts",
                       "BBI", "Avg", "Econ", "SR", "4w", "5w"
                       ]

        filepath_cric = "csv files/BOWLING STATS - IPL_2022.csv"

    # except IndexError:
    #     st.info(player + " might not have been auctioned.")
    #     player_role = 'player'

    try:
        data = pd.read_csv(filepath_cric)
    except FileNotFoundError:
        st.warning("Woah there! pardner",
                   icon='🤠')

    try:
        with st.sidebar:

            # index argument changes the values which col_pl is referring to
            option = st.selectbox("Select data to view for the specific player",
                                  col_pl,
                                  key='player_op',
                                  index=2)

            col_pl.remove(option)

            option_2 = st.selectbox("Select data to view for the specific player",
                                    col_pl,
                                    key='player_op_2',
                                    index=6)

        player_value = data.loc[data['Player'] == player, (option, option_2)].values[0]
        st.info(f"{player} is a {player_role} whose {option} is/are {player_value[0]} " +
                f"and the {option_2} is/are {player_value[1]}.")

        num_play = st.slider("What is the range of players you want to get details of ?", value=(1, 162),
                             help="Batters = 162, Bowlers = 103 ")
        num_col = st.slider("What is the range of columns you want to see?", value=(1, 14),
                            help="Columns = 14")

        disp_col = col_pl_temp[num_col[0]:num_col[1]]

        st.write(data[disp_col][num_play[0]:num_play[1]])

    except IndexError:
        st.info(player + " is not in player stats database you are referring to")
    except ValueError:
        st.warning("Please enter a player name.")

# st.toast('Woah!')
