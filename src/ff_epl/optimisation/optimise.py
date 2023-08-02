import pandas as pd
import pulp

from pathlib import Path


def fetch_data(filepath: Path) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    df["injured"] = 0  # Return no players injured (update at runtime)
    df["now_cost"] = df["now_cost"]
    return df


def generate_model(
        df: pd.DataFrame, optimisation_metric: str = "total_points"
        ) -> tuple[list[pulp.LpVariable], pulp.LpProblem]:
    # Decision variables
    X = [pulp.LpVariable("x_{}".format(i), cat="Binary") for i in df.index]

    # Binary vectors to filter for player positions
    B_gkr = (df["position"] == "GKP").astype(int)
    B_def = (df["position"] == "DEF").astype(int)
    B_mid = (df["position"] == "MID").astype(int)
    B_fwd = (df["position"] == "FWD").astype(int)

    # Binary vectors to filter for injured players
    B_inj = df["injured"].astype(int)

    # Continuous variables to count player positions needed for bench
    C_gkr = pulp.LpVariable("C_gk", cat="Continuous")
    C_def = pulp.LpVariable("C_def", cat="Continuous")
    C_mid = pulp.LpVariable("C_mid", cat="Continuous")
    C_fwd = pulp.LpVariable("C_fwd", cat="Continuous")

    # Get minimum Costs for each position
    mC_gkr = df[df["position"] == "GKP"]["now_cost"].min()
    mC_def = df[df["position"] == "DEF"]["now_cost"].min()
    mC_mid = df[df["position"] == "MID"]["now_cost"].min()
    mC_fwd = df[df["position"] == "FWD"]["now_cost"].min()

    # Instantiate model
    mdl = pulp.LpProblem("FantasyFootball", pulp.LpMaximize)

    # Objective Function
    mdl += sum(X[i] * df.loc[i, optimisation_metric] for i in df.index), "Objective"

    # Constraints
    # Team selection
    mdl += sum(X) == 11, "Con_EQ_TeamCount"
    mdl += sum(X[i] * B_gkr[i] for i in df.index) == 1, "Con_EQ1_Goalkeepers"
    mdl += sum(X[i] * B_def[i] for i in df.index) >= 3, "Con_GE3_Defenders"
    mdl += sum(X[i] * B_def[i] for i in df.index) <= 5, "Con_LE5_Defenders"
    mdl += sum(X[i] * B_mid[i] for i in df.index) <= 5, "Con_LE5_Midfielders"
    mdl += sum(X[i] * B_fwd[i] for i in df.index) >= 1, "Con_GE1_Forwards"
    # Get how many more players for bench
    mdl += sum(X[i] * B_gkr[i] for i in df.index) + C_gkr == 2, "Con_EQ_GoalkeepersCount"
    mdl += sum(X[i] * B_def[i] for i in df.index) + C_def == 5, "Con_EQ_DefendersCount"
    mdl += sum(X[i] * B_mid[i] for i in df.index) + C_mid == 5, "Con_EQ_MidfieldersCount"
    mdl += sum(X[i] * B_fwd[i] for i in df.index) + C_fwd == 3, "Con_EQ_ForwardsCount"
    # Use player count to adjust total cost (need to buy bench)
    mdl += sum(X[i] * df.loc[i, "now_cost"] for i in df.index) + mC_gkr * C_gkr + mC_def * C_def\
    + mC_mid * C_mid + mC_fwd * C_fwd <= 100, "Con_LE_SquadCost"
    # Max. three players from each team
    for team in df["club"].unique():
        B_team = (df["club"] == team).astype(int)
        mdl += sum(X[i] * B_team[i] for i in df.index) <= 3, f"Con_LE_Max{team}Count"
    # Avoid injured players
    mdl += sum(X[i] * B_inj[i] for i in df.index) == 0, "Con_EQ_AvoidInjuries"
    return X, mdl


def lpsolve(model: pulp.LpProblem, logs: bool = True) -> None:
    model.solve(pulp.PULP_CBC_CMD(msg=logs))


def main() -> None:
    df = fetch_data(r"data/player_points.csv")
    decision_vars, mdl = generate_model(df)
    mdl.writeLP("FantasyFootball.lp")  # Output human readable LP file
    mdl.solve()
    # Get solution vector
    SV = [bool(int(x.value())) for x in decision_vars]
    print(f'Team cost: ${df[SV]["now_cost"].sum(): .2f}')
    print(df[SV])


if __name__ == "__main__":
    main()
