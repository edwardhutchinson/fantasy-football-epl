import concurrent.futures
from pathlib import Path

from ff_epl.data_sourcing. get_data import fetch_players, fetch_players_history


def main():
    data_dir = Path.cwd() / "data"

    if data_dir.exists():
        print(f"Directory {data_dir} already exists, wipe data inside and regenerate? (Y/n)")
        if input("-> ") == "Y":
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(Path.unlink, data_dir.glob("*.csv"))
        else:
            return

    data_dir.mkdir(exist_ok=True)

    player_ids = fetch_players(data_directory=data_dir)
    fetch_players_history(player_ids=player_ids, data_directory=data_dir)


if __name__ == '__main__':
    main()
