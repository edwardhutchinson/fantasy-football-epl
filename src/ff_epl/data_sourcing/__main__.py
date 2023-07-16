from ff_epl.data_sourcing. get_data import fetch_players, fetch_player_history_data

def main():
    df = fetch_players()
    fetch_player_history_data(df.index)


if __name__ == '__main__':
    main()
