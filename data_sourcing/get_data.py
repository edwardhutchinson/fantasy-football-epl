import pandas as pd
import requests


def fetch_data(end_point, url='https://fantasy.premierleague.com/api/{}'):
    """Fetch data from https://fantasy.premierleague.com API."""
    r = requests.get(url.format(end_point))
    j = r.json()
    return j


def fetch_players():
    """Fetch top level player data with current season stats (if ongoing).
    Returns player DataFrame and saves to '../data/players.csv'."""
    data = fetch_data('bootstrap-static/')
    # Player data
    players = pd.json_normalize(data['elements'])[[
        'first_name',
        'second_name',
        'id',
        'team_code',
        'element_type',
        'now_cost',
        # 'total_points',
        # 'points_per_game', 
        # 'minutes'
    ]].rename(columns={'element_type': 'pos_code'})
    # Team data to add to player information (needed for <= 3 players each team)
    teams = pd.json_normalize(data['teams'])[[
        'code',
        'name',
        'short_name'
    ]]
    # Position data (needed as player DataFrame uses a position code...)
    positions = pd.json_normalize(data['element_types'])[[
        'id',
        'singular_name_short'
    ]].rename(columns={'id':'code', 'singular_name_short':'position'})
    # Left join, add what we can to player DataFrame
    df = players.set_index('team_code').join(
        teams.set_index('code'), how='left').reset_index(drop=True)
    df = df.set_index('pos_code').join(
        positions.set_index('code'), how='left').reset_index(drop=True)
    df = df.set_index('id')
    # Export
    df.to_csv('../data/players.csv')
    # Return DataFrame too for more detailed data collection
    return df


def fetch_player_history_data(player_ids):
    """Fetch a player's history data (season by season). Saves data to '../data/p_{player_id}.csv'."""
    for id in player_ids:
        d = fetch_data(f'element-summary/{id}/')
        if d['history_past'] == []:  # don't save csv of no data
            continue
        df = pd.json_normalize(d['history_past'])
        df.to_csv(f'../data/p_{id}.csv', index=False)


def main():
    df = fetch_players()
    fetch_player_history_data(df.index)


if __name__ == '__main__':
    main()