import concurrent.futures
import pandas as pd
import requests

from pathlib import Path
from typing import Any


def fetch_data(end_point: str, url: str = "https://fantasy.premierleague.com/api/{}") -> dict[str, Any]:
    r = requests.get(url.format(end_point))
    return r.json()

def fetch_players(data_directory: Path) -> list[int]:
    """Fetch top level player data with current season stats (if ongoing).
    Returns player DataFrame and saves to "../data/players.csv"."""
    data = fetch_data("bootstrap-static/")
    # Player data
    players = pd.json_normalize(data["elements"])[[
        "first_name",
        "second_name",
        "id",
        "team_code",
        "element_type",
        "now_cost",
        # "total_points",
        # "points_per_game", 
        # "minutes"
    ]].rename(columns={"element_type": "pos_code"})
    # Team data to add to player information (needed for <= 3 players each team)
    teams = pd.json_normalize(data["teams"])[[
        "code",
        "name",
        "short_name"
    ]]
    # Position data (needed as player DataFrame uses a position code...)
    positions = pd.json_normalize(data["element_types"])[[
        "id",
        "singular_name_short"
    ]].rename(columns={"id":"code", "singular_name_short":"position"})
    # Left join, add what we can to player DataFrame
    df = players.set_index("team_code").join(
        teams.set_index("code"), how="left").reset_index(drop=True)
    df = df.set_index("pos_code").join(
        positions.set_index("code"), how="left").reset_index(drop=True)
    df = df.set_index("id")
    # Export
    df.to_csv(data_directory / "players.csv")
    # Return DataFrame too for more detailed data collection
    return list(df.index)

def fetch_player_history(player_id: int, data_directory: Path) -> pd.DataFrame:
    d = fetch_data(f"element-summary/{player_id}/")
    if d["history_past"]:
        df = pd.json_normalize(d["history_past"])
        df.to_csv(f"{data_directory}/p_{player_id}.csv", index=False)

def fetch_players_history(player_ids: list[int], data_directory: Path) -> None:
    """Fetch a player"s history data (season by season). Saves data to "../data/p_{player_id}.csv"."""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(fetch_player_history, player_ids, [data_directory] * len(player_ids))
