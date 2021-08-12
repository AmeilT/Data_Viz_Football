from chart_functions import create_expected_player_graph, hbarplot_players,stacked_hbarplot_players, cumm_calc_gw,namescleaner,create_expected_goals_player_graph
from constants import features, teams
import pandas as pd
import os
from pathlib import Path

def expected_player_goals(season, gameweek_range):
    # Import data
    season = season
    cwd = Path(os.getcwd())
    dict_path = {}

    for feature in features:
        dict_path[
            f"{feature}_data_path"] = rf"{str(cwd.parent.absolute())}/FFScout Database/scraper/data/player data/{feature}_{season}"

    dict_data = {}
    for feature in features:
        dict_data[f"{feature}_data"] = pd.read_csv(dict_path[f"{feature}_data_path"])
        dict_data[f"{feature}_data"] = dict_data[f"{feature}_data"].merge(teams, on='Team', how='inner')
        dict_data[f"{feature}_data"]["Name"] = dict_data[f"{feature}_data"]["Name"].apply(namescleaner)

    # Filter data
    # gameweek_range = [37, 38]
    A = gameweek_range[0]
    B = gameweek_range[1]

    for key, value in dict_data.items():
        dict_data[key] = value.loc[(value['Gameweek'] >= A) & (value['Gameweek'] <= B)]

    # Graph Inputs
    data = "expected_data"
    method = "sum"
    if method == "mean":
        df = dict_data[data].groupby(["Name", "Team", "Colours"]).mean().reset_index()
    elif method == "sum":
        df = dict_data[data].groupby(["Name", "Team", "Position", "Colours"]).sum().reset_index()

    x1 = "GoalsG"
    x2 = "GoalsxG"
    y = "Name"

    # xG vs G graph
    df_1 = df[(df[x1] > 0) & (df["Position"] == "Defender") | (df[x2] >= 0.3) & (df["Position"] == "Defender") & (
                df[x1] == 0)]
    create_expected_goals_player_graph(df_1, x1, x2, y, "Actual Goals", "Expected Goals", "Actual vs Expected Goals Scored",
                                 gameweekrange=gameweek_range)
    df_1 = df[(df[x1] > 0) & (df["Position"] == "Midfielder") | (df[x2] >= 0.5) & (df["Position"] == "Midfielder") & (
                df[x1] == 0)]
    create_expected_goals_player_graph(df_1, x1, x2, y, "Actual Goals", "Expected Goals", "Actual vs Expected Goals Scored",
                                 gameweekrange=gameweek_range)
    df_1 = df[
        (df[x1] > 0) & (df["Position"] == "Forward") | (df[x2] >= 0.5) & (df["Position"] == "Forward") & (df[x1] == 0)]
    create_expected_goals_player_graph(df_1, x1, x2, y, "Actual Goals", "Expected Goals", "Actual vs Expected Goals Scored",
                                 gameweekrange=gameweek_range)

    # plot top X overacheivers
    N = 15
    df_1 = df[(df["GoalsG"] > 1)]
    df_1 = df_1.sort_values(by=["GoalsΔ"], ascending=False)
    hbarplot_players(df_1, x1, x2, y, "Goals Scored", "Expected Goals","", f"Top {N} overperformers by xG", gameweekrange=gameweek_range)

    # plot top 10 underacheivers
    N = 15
    df_1 = df[(df["GoalsxG"]) > 0.1]
    df_2 = df.sort_values(by=["GoalsΔ"], ascending=True).head(N)
    hbarplot_players(df_2, x1, x2, y, "Goals Scored", "Expected Goals","", f"Top {N} underperformers by xG", gameweekrange=gameweek_range)

    # plot together

    # plot top xG
    N = 15
    df_1 = df
    df_1 = df_1.sort_values(by=["GoalsxG"], ascending=False).head(N)
    hbarplot_players(df_1, x1, x2, y, "Goals Scored", "Expected Goals","", f"Top {N} players by xG", gameweekrange=gameweek_range)

    # Plot stacked xG by Gameweek
    df_stacked = dict_data[data][["Name", "Gameweek", "GoalsxG"]]
    gw_list = list(df_stacked["Gameweek"].unique())

    test = pd.pivot_table(df_stacked, index='Name', values='GoalsxG', columns='Gameweek')
    test = cumm_calc_gw(test, gw_list, N)
    stacked_hbarplot_players(test, "Name", "xG", f"Top {N} players by xG", gameweekrange=gameweek_range)

    df_stacked = dict_data[data][["Name", "Gameweek", "GoalsxG", "Position"]]
    df_stacked_def = df_stacked[df_stacked["Position"] == "Defender"]
    df_stacked_mid = df_stacked[df_stacked["Position"] == "Midfielder"]
    df_stacked_fwd = df_stacked[df_stacked["Position"] == "Forward"]

    test = pd.pivot_table(df_stacked_def, index='Name', values='GoalsxG', columns='Gameweek')
    test = cumm_calc_gw(test, gw_list, N)
    stacked_hbarplot_players(test, "Name", "xG", f"Top {N} Defenders by xG", gameweekrange=gameweek_range)
    test = pd.pivot_table(df_stacked_mid, index='Name', values='GoalsxG', columns='Gameweek')
    test = cumm_calc_gw(test, gw_list, N)
    stacked_hbarplot_players(test, "Name", "xG", f"Top {N} Midfielders by xG", gameweekrange=gameweek_range)
    test = pd.pivot_table(df_stacked_fwd, index='Name', values='GoalsxG', columns='Gameweek')
    test = cumm_calc_gw(test, gw_list, N)
    stacked_hbarplot_players(test, "Name", "xG", f"Top {N} Forwards by xG", gameweekrange=gameweek_range)

def expected_player_involvement(season, gameweek_range):
    # Import data
    season = season
    cwd = Path(os.getcwd())
    dict_path = {}

    for feature in features:
        dict_path[
            f"{feature}_data_path"] = rf"{str(cwd.parent.absolute())}/FFScout Database/scraper/data/player data/{feature}_{season}"

    dict_data = {}
    for feature in features:
        dict_data[f"{feature}_data"] = pd.read_csv(dict_path[f"{feature}_data_path"])
        dict_data[f"{feature}_data"] = dict_data[f"{feature}_data"].merge(teams, on='Team', how='inner')
        dict_data[f"{feature}_data"]["Name"] = dict_data[f"{feature}_data"]["Name"].apply(namescleaner)

    # Filter data
    # gameweek_range = [37, 38]
    A = gameweek_range[0]
    B = gameweek_range[1]

    for key, value in dict_data.items():
        dict_data[key] = value.loc[(value['Gameweek'] >= A) & (value['Gameweek'] <= B)]

    # Graph Inputs
    data = "expected_data"
    method = "sum"
    dict_data[data]["InvolvementGI"]=dict_data[data]["GoalsG"]+dict_data[data]["AssistsA"]
    if method == "mean":
        df = dict_data[data].groupby(["Name", "Team", "Colours"]).mean().reset_index()
    elif method == "sum":
        df = dict_data[data].groupby(["Name", "Team", "Position", "Colours"]).sum().reset_index()

    x1 = "InvolvementGI"
    x2 = "InvolvementxGI"
    y = "Name"

    # xGI vs GI graph
    df_1 = df[(df[x1] > 0) & (df["Position"] == "Defender") | (df[x2] >= 0.2) & (df["Position"] == "Defender") & (
                df[x1] == 0)]
    create_expected_player_graph(df_1, x1, x2, y, "Actual Goal Involvements", "Expected Goal Involvements", "Actual vs Expected Goal Involvements",
                                 gameweekrange=gameweek_range)
    df_1 = df[(df[x1] > 0) & (df["Position"] == "Midfielder") | (df[x2] >= 0.5) & (df["Position"] == "Midfielder") & (
                df[x1] == 0)]
    create_expected_player_graph(df_1, x1, x2, y, "Actual Goal Involvements", "Expected Goal Involvements", "Actual vs Expected Goal Involvements",
                                 gameweekrange=gameweek_range)
    df_1 = df[
        (df[x1] > 0) & (df["Position"] == "Forward") | (df[x2] >= 0.5) & (df["Position"] == "Forward") & (df[x1] == 0)]
    create_expected_player_graph(df_1, x1, x2, y, "Actual Goal Involvements", "Expected Goal Involvements", "Actual vs Expected Goal Involvements",
                                 gameweekrange=gameweek_range)

    # plot top X overacheivers
    N = 15
    df_1 = df[(df["InvolvementGI"] > 1)]
    df_1 = df_1.sort_values(by=["InvolvementΔ"], ascending=False).head(N)
    hbarplot_players(df_1, x1, x2, y, "", "", f"Top {N} overperformers by xGI", gameweekrange=gameweek_range)

    # plot top 10 underacheivers
    N = 15
    df_1 = df[(df["InvolvementxGI"]) > 0.1]
    df_2 = df.sort_values(by=["InvolvementΔ"], ascending=True).head(N)
    hbarplot_players(df_2, x1, x2, y, "", "", f"Top {N} underperformers by xGI", gameweekrange=gameweek_range)

    # plot together

    # plot top xG
    N = 15
    df_1 = df
    df_1 = df_1.sort_values(by=["InvolvementxGI"], ascending=False).head(N)
    hbarplot_players(df_1, x1, x2, y, "", "", f"Top {N} players by xGI", gameweekrange=gameweek_range)

    # Plot stacked xG by Gameweek
    df_stacked = dict_data[data][["Name", "Gameweek", "InvolvementxGI"]]
    gw_list = list(df_stacked["Gameweek"].unique())

    test = pd.pivot_table(df_stacked, index='Name', values='InvolvementxGI', columns='Gameweek')
    test = cumm_calc_gw(test, gw_list, N)
    stacked_hbarplot_players(test, "Name", "xG", f"Top {N} players by xGI", gameweekrange=gameweek_range)

    df_stacked = dict_data[data][["Name", "Gameweek", "InvolvementxGI", "Position"]]
    df_stacked_def = df_stacked[df_stacked["Position"] == "Defender"]
    df_stacked_mid = df_stacked[df_stacked["Position"] == "Midfielder"]
    df_stacked_fwd = df_stacked[df_stacked["Position"] == "Forward"]

    test = pd.pivot_table(df_stacked_def, index='Name', values='InvolvementxGI', columns='Gameweek')
    test = cumm_calc_gw(test, gw_list, N)
    stacked_hbarplot_players(test, "Name", "xG", f"Top {N} Defenders by xGI", gameweekrange=gameweek_range)
    test = pd.pivot_table(df_stacked_mid, index='Name', values='InvolvementxGI', columns='Gameweek')
    test = cumm_calc_gw(test, gw_list, N)
    stacked_hbarplot_players(test, "Name", "xG", f"Top {N} Midfielders by xGI", gameweekrange=gameweek_range)
    test = pd.pivot_table(df_stacked_fwd, index='Name', values='InvolvementxGI', columns='Gameweek')
    test = cumm_calc_gw(test, gw_list, N)
    stacked_hbarplot_players(test, "Name", "xG", f"Top {N} Forwards by xGI", gameweekrange=gameweek_range)

def distribution_player_chances(season, gameweek_range):
    # Import data
    season = season
    cwd = Path(os.getcwd())
    dict_path = {}

    for feature in features:
        dict_path[
            f"{feature}_data_path"] = rf"{str(cwd.parent.absolute())}/FFScout Database/scraper/data/player data/{feature}_{season}"

    dict_data = {}
    for feature in features:
        dict_data[f"{feature}_data"] = pd.read_csv(dict_path[f"{feature}_data_path"])
        dict_data[f"{feature}_data"] = dict_data[f"{feature}_data"].merge(teams, on='Team', how='inner')
        dict_data[f"{feature}_data"]["Name"] = dict_data[f"{feature}_data"]["Name"].apply(namescleaner)

    # Filter data
    gameweek_range = gameweek_range
    A = gameweek_range[0]
    B = gameweek_range[1]

    for key, value in dict_data.items():
        dict_data[key] = value.loc[(value['Gameweek'] >= A) & (value['Gameweek'] <= B)]

    # Graph Inputs
    data = "distribution_data"
    method = "sum"
    if method == "mean":
        df = dict_data[data].groupby(["Name", "Team", "Colours"]).mean().reset_index()
    elif method == "sum":
        df = dict_data[data].groupby(["Name", "Team", "Position", "Colours"]).sum().reset_index()

    x1 = "Assist PotentialBCC"
    x2 = "Assist PotentialCC"
    y = "Name"
    x1_text = "Big Chances Created"
    x2_text = "Chances Created"

    # xGI vs GI graph
    df_1 = df[(df[x1] > 1) & (df["Position"] == "Defender")]
    create_expected_player_graph(df_1, x1, x2, y, x1_text, x2_text, f"{x1_text} vs {x2_text}:Defenders",
                                 gameweekrange=gameweek_range)
    df_1 = df[(df[x1] > 1) & (df["Position"] == "Midfielder")]
    create_expected_player_graph(df_1, x1, x2, y, x1_text, x2_text, f"{x1_text} vs {x2_text}:Midfielders",
                                 gameweekrange=gameweek_range)
    df_1 = df[(df[x1] > 1) & (df["Position"] == "Forward")]
    create_expected_player_graph(df_1, x1, x2, y, x1_text, x2_text, f"{x1_text} vs {x2_text}:Forwards",
                                 gameweekrange=gameweek_range)

    df_1 = df[(df[x1] > 0) & (df[x2] > 0)]
    create_expected_player_graph(df_1, x1, x2, y, x1_text, x2_text, f"{x1_text} vs {x2_text}",
                                 gameweekrange=gameweek_range)

    # plot top BCC
    N = 15
    df_1 = df
    df_1 = df_1.sort_values(by=[x2], ascending=False).head(N)
    hbarplot_players(df_1, x1, x2, y, "Chances Created", f"Top {N} players by {x2_text}", gameweekrange=gameweek_range)

    # Plot stacked CC by Gameweek
    df_stacked = dict_data[data][["Name", "Gameweek", x2]]
    gw_list = list(df_stacked["Gameweek"].unique())

    test = pd.pivot_table(df_stacked, index='Name', values=x2, columns='Gameweek')
    test = cumm_calc_gw(test, gw_list, N)
    stacked_hbarplot_players(test, "Name", "Chances Created", f"Top {N} players by {x2_text}", gameweekrange=gameweek_range)

    df_stacked = dict_data[data][["Name", "Gameweek", x2, "Position"]]
    df_stacked_def = df_stacked[df_stacked["Position"] == "Defender"]
    df_stacked_mid = df_stacked[df_stacked["Position"] == "Midfielder"]
    df_stacked_fwd = df_stacked[df_stacked["Position"] == "Forward"]

    test = pd.pivot_table(df_stacked_def, index='Name', values=x2, columns='Gameweek')
    test = cumm_calc_gw(test, gw_list, N)
    stacked_hbarplot_players(test, "Name", "Chances Created", f"Top {N} Defenders by {x2_text}", gameweekrange=gameweek_range)
    test = pd.pivot_table(df_stacked_mid, index='Name', values=x2, columns='Gameweek')
    test = cumm_calc_gw(test, gw_list, N)
    stacked_hbarplot_players(test, "Name", "Chances Created", f"Top {N} Midfielders by {x2_text}", gameweekrange=gameweek_range)
    test = pd.pivot_table(df_stacked_fwd, index='Name', values=x2, columns='Gameweek')
    test = cumm_calc_gw(test, gw_list, N)
    stacked_hbarplot_players(test, "Name","Chances Created", f"Top {N} Forwards by {x2_text}", gameweekrange=gameweek_range)

def attempts_player(season,gameweek_range):
    # Import data
    season = season
    cwd = Path(os.getcwd())
    dict_path = {}

    for feature in features:
        dict_path[
            f"{feature}_data_path"] = rf"{str(cwd.parent.absolute())}/FFScout Database/scraper/data/player data/{feature}_{season}"

    dict_data = {}
    for feature in features:
        dict_data[f"{feature}_data"] = pd.read_csv(dict_path[f"{feature}_data_path"])
        dict_data[f"{feature}_data"] = dict_data[f"{feature}_data"].merge(teams, on='Team', how='inner')
        dict_data[f"{feature}_data"]["Name"] = dict_data[f"{feature}_data"]["Name"].apply(namescleaner)

    # Filter data
    gameweek_range = gameweek_range
    A = gameweek_range[0]
    B = gameweek_range[1]

    for key, value in dict_data.items():
        dict_data[key] = value.loc[(value['Gameweek'] >= A) & (value['Gameweek'] <= B)]

    # Graph Inputs
    data = "goal-threat_data"
    method = "sum"
    if method == "mean":
        df = dict_data[data].groupby(["Name", "Team", "Colours"]).mean().reset_index()
    elif method == "sum":
        df = dict_data[data].groupby(["Name", "Team", "Position", "Colours"]).sum().reset_index()

    x1 = "AttemptsTot"
    x2 = "AttemptsIn"
    y = "Name"
    x1_text = "Total Attempts"
    x2_text = "Attempts in Box"

    # xGI vs GI graph
    df_1 = df[(df[x1] > 1) & (df["Position"] == "Defender")]
    create_expected_player_graph(df_1, x1, x2, y, x1_text, x2_text, f"{x1_text} vs {x2_text}:Defenders",
                                 gameweekrange=gameweek_range)
    df_1 = df[(df[x1] > 1) & (df["Position"] == "Midfielder")]
    create_expected_player_graph(df_1, x1, x2, y, x1_text, x2_text, f"{x1_text} vs {x2_text}:Midfielders",
                                 gameweekrange=gameweek_range)
    df_1 = df[(df[x1] > 1) & (df["Position"] == "Forward")]
    create_expected_player_graph(df_1, x1, x2, y, x1_text, x2_text, f"{x1_text} vs {x2_text}:Forwards",
                                 gameweekrange=gameweek_range)

    df_1 = df[(df[x1] > 0) & (df[x2] > 0)]
    create_expected_player_graph(df_1, x1, x2, y, x1_text, x2_text, f"{x1_text} vs {x2_text}",
                                 gameweekrange=gameweek_range)

    # plot top BCC
    N = 15
    df_1 = df
    df_1 = df_1.sort_values(by=[x2], ascending=False).head(N)
    hbarplot_players(df_1, x1, x2, y, "", f"Top {N} players by {x2_text}", gameweekrange=gameweek_range)

    # Plot stacked CC by Gameweek
    df_stacked = dict_data[data][["Name", "Gameweek", x2]]
    gw_list = list(df_stacked["Gameweek"].unique())

    test = pd.pivot_table(df_stacked, index='Name', values=x2, columns='Gameweek')
    test = cumm_calc_gw(test, gw_list, N)
    stacked_hbarplot_players(test, "Name", f"{x2_text}", f"Top {N} players by {x2_text}", gameweekrange=gameweek_range)

    df_stacked = dict_data[data][["Name", "Gameweek", x2, "Position"]]
    df_stacked_def = df_stacked[df_stacked["Position"] == "Defender"]
    df_stacked_mid = df_stacked[df_stacked["Position"] == "Midfielder"]
    df_stacked_fwd = df_stacked[df_stacked["Position"] == "Forward"]

    test = pd.pivot_table(df_stacked_def, index='Name', values=x2, columns='Gameweek')
    test = cumm_calc_gw(test, gw_list, N)
    stacked_hbarplot_players(test, "Name", f"{x2_text}", f"Top {N} Defenders by {x2_text}",
                             gameweekrange=gameweek_range)
    test = pd.pivot_table(df_stacked_mid, index='Name', values=x2, columns='Gameweek')
    test = cumm_calc_gw(test, gw_list, N)
    stacked_hbarplot_players(test, "Name", f"{x2_text}", f"Top {N} Midfielders by {x2_text}",
                             gameweekrange=gameweek_range)
    test = pd.pivot_table(df_stacked_fwd, index='Name', values=x2, columns='Gameweek')
    test = cumm_calc_gw(test, gw_list, N)
    stacked_hbarplot_players(test, "Name", f"{x2_text}", f"Top {N} Forwards by {x2_text}", gameweekrange=gameweek_range)

def touches_player_attempts(season,gameweek_range,x1min,x2min):
    # Import data
    season = season
    cwd = Path(os.getcwd())
    dict_path = {}

    for feature in features:
        dict_path[
            f"{feature}_data_path"] = rf"{str(cwd.parent.absolute())}/FFScout Database/scraper/data/player data/{feature}_{season}"

    dict_data = {}
    for feature in features:
        dict_data[f"{feature}_data"] = pd.read_csv(dict_path[f"{feature}_data_path"])
        dict_data[f"{feature}_data"] = dict_data[f"{feature}_data"].merge(teams, on='Team', how='inner')
        dict_data[f"{feature}_data"]["Name"] = dict_data[f"{feature}_data"]["Name"].apply(namescleaner)

    # Filter data
    gameweek_range = gameweek_range
    A = gameweek_range[0]
    B = gameweek_range[1]

    for key, value in dict_data.items():
        dict_data[key] = value.loc[(value['Gameweek'] >= A) & (value['Gameweek'] <= B)]

    # Graph Inputs
    data = "goal-threat_data"
    method = "sum"
    if method == "mean":
        df = dict_data[data].groupby(["Name", "Team", "Colours"]).mean().reset_index()
    elif method == "sum":
        df = dict_data[data].groupby(["Name", "Team", "Position", "Colours"]).sum().reset_index()

    x1 = "Unnamed: 6_level_0Pen Tchs"
    x2 = "AttemptsIn"
    y = "Name"
    x1_text = "Penalty Touches"
    x2_text = "Attempts in Box"

    # xGI vs GI graph
    df_1 = df[(df[x1] > x1min) & (df["Position"] == "Defender")|(df[x1] > x1min) & (df["Position"] == "Defender")]
    create_expected_player_graph(df_1, x1, x2, y, x1_text, x2_text, f"{x1_text} vs {x2_text}: Defenders",
                                 gameweekrange=gameweek_range)
    df_1 = df[(df[x1] > x1min) & (df["Position"] == "Midfielder")]
    create_expected_player_graph(df_1, x1, x2, y, x1_text, x2_text, f"{x1_text} vs {x2_text}: Midfielders",
                                 gameweekrange=gameweek_range)
    df_1 = df[(df[x1] > x1min) & (df["Position"] == "Forward")]
    create_expected_player_graph(df_1, x1, x2, y, x1_text, x2_text, f"{x1_text} vs {x2_text}: Forwards",
                                 gameweekrange=gameweek_range)

    df_1 = df[(df[x1] > x1min) & (df[x2] > x2min)]
    create_expected_player_graph(df_1, x1, x2, y, x1_text, x2_text, f"{x1_text} vs {x2_text}",
                                 gameweekrange=gameweek_range)

    # plot top BCC
    N = 15
    df_1 = df
    df_1 = df_1.sort_values(by=[x2], ascending=False).head(N)
    hbarplot_players(df_1, x1, x2, y, "", f"Top {N} players by {x2_text}", gameweekrange=gameweek_range)

