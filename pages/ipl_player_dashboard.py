import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
from utils import load_data, get_player_stats

# Load the data
data = load_data('ipl_data.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("IPL Player Stats Dashboard"),
    dcc.Dropdown(
        id='player-dropdown',
        options=[{'label': player, 'value': player} for player in data['player_of_match'].unique()],
        value=data['player_of_match'].unique()[0]
    ),
    dcc.RadioItems(
        id='stat-type-radio',
        options=[
            {'label': 'Batting', 'value': 'batting'},
            {'label': 'Bowling', 'value': 'bowling'}
        ],
        value='batting',
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id='player-graph'),
])

# Callback to update graph based on selected player and stat type
@app.callback(
    dash.Output('player-graph', 'figure'),
    [dash.Input('player-dropdown', 'value'),
     dash.Input('stat-type-radio', 'value')]
)
def update_graph(selected_player, selected_stat_type):
    player_stats = get_player_stats(data, selected_player, selected_stat_type)
    fig = px.bar(player_stats, x='stat', y='value', color='stat', title=f'{selected_player} {selected_stat_type.capitalize()} Stats')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)