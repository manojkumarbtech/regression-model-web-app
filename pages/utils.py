import pandas as pd

def load_data(filepath):
    """Load the IPL data from a CSV file."""
    return pd.read_csv(filepath)

def get_groundwise_data(data, venue):
    """Get ground-wise data for the selected venue."""
    ground_data = data[data['venue'] == venue]
    wins = ground_data['winner'].value_counts().reset_index()
    wins.columns = ['team', 'wins']
    return wins

def get_player_stats(data, player, stat_type):
    """Get player stats for the selected player and stat type."""
    player_data = data[data['player_of_match'] == player]
    matches = len(player_data)
    wins = player_data['winner'].value_counts().get(player, 0)
    
    if stat_type == 'batting':
        # Example batting stats: matches, runs, average
        runs = player_data['win_by_runs'].sum()  # Example placeholder
        average = runs / matches if matches > 0 else 0
        stats = pd.DataFrame({'stat': ['Matches', 'Runs', 'Average'], 'value': [matches, runs, average]})
    elif stat_type == 'bowling':
        # Example bowling stats: matches, wickets, economy
        wickets = player_data['win_by_wickets'].sum()  # Example placeholder
        economy = wickets / matches if matches > 0 else 0
        stats = pd.DataFrame({'stat': ['Matches', 'Wickets', 'Economy'], 'value': [matches, wickets, economy]})
    
    return stats