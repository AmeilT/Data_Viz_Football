from Viz_Chart_Functions import create_expected_player_graph, stacked_hbarplot_players_grid,\
    hbarplot_players_grid,hbarplot_players_colours,hbarplot_players_colours_hatch,create_expected_player_graph_size
from constants.constants import *
import os
os.chdir(path)


def hbar_player(df, variables, season, gameweek_range, sort, x1_title, x2_title, y, N,sort_name):
    # Sum over mins per name and per season
    columns = ["Name", "Season", "Gameweek", "Position", "Mins", "Colours"]
    PL_data_all = df[columns + variables]
    PL_data_all_sum = PL_data_all.groupby(["Name", "Season", "Position", "Colours"]).sum().reset_index()
    for x in variables:
        PL_data_all_sum[f"{x} per 90"] = PL_data_all_sum[x] * 90 / PL_data_all_sum["Mins"]
    PL_data_all_sum = PL_data_all_sum[PL_data_all_sum["Mins"] > 1600]

    # Filter by current season
    PL_data_season = df[df["Season"] == season]

    # Filter data by GW range
    A = gameweek_range[0]
    B = gameweek_range[1]
    PL_data_season_filter = PL_data_season[(PL_data_season['Gameweek'] >= A) & (PL_data_season['Gameweek'] <= B)]

    x1 = variables[0]
    x2 = variables[1]

    # plot top X player_scatter
    filepath=f"Top {N} overperformers by {sort_name}"
    df_1 = PL_data_season_filter[(PL_data_season_filter[x1] >= 1)]
    hbarplot_players_grid(df_1, gameweek_range, N, sort_name, filepath,
                                  x1,x2,x1_title, x2_title,f"Top {N} overperformers by {sort_name}",sort,boo=False)

    # plot top X underacheivers
    filepath=f"Top {N} underperformers by {sort_name}"
    df_1 = PL_data_season_filter[(PL_data_season_filter[x2]) > 0]
    hbarplot_players_grid(df_1, gameweek_range, N, sort_name, filepath,
                          x1, x2, x1_title, x2_title, f"Top {N} underperformers by {sort_name}", sort,boo=True)
    # plot top xGI
    filepath=f"Top {N} players by {sort_name}"
    df_1 = PL_data_season_filter
    df_1 = df_1.sort_values(by=[x2], ascending=False).head(N)

    hbarplot_players_colours(df_1, x2, y, x2_title, "", f"Top {N} players by {sort_name}",
                             gameweekrange=gameweek_range, positions=positions,filepath=filepath)

    # Plot stacked xG by Gameweek
    df_stacked = PL_data_season_filter[["Name", "Gameweek", x2]]
    stacked_hbarplot_players_grid(PL_data_season_filter, gameweek_range, N, sort_name, filepath,
                                  x2, x2_title)
def hbar_player_hatch(df, variables, season, gameweek_range, sort, x1_title, x2_title, y, N,sort_name):
    # Sum over mins per name and per season
    columns = ["Name", "Season", "Gameweek", "Position", "Mins", "Colours"]
    PL_data_all = df[columns + variables]
    PL_data_all_sum = PL_data_all.groupby(["Name", "Season", "Position", "Colours"]).sum().reset_index()
    for x in variables:
        PL_data_all_sum[f"{x} per 90"] = PL_data_all_sum[x] * 90 / PL_data_all_sum["Mins"]
    PL_data_all_sum = PL_data_all_sum[PL_data_all_sum["Mins"] > 1600]

    # Filter by current season
    PL_data_season = df[df["Season"] == season]

    # Filter data by GW range
    A = gameweek_range[0]
    B = gameweek_range[1]
    PL_data_season_filter = PL_data_season[(PL_data_season['Gameweek'] >= A) & (PL_data_season['Gameweek'] <= B)]

    x1 = variables[0]
    x2 = variables[1]
    x3 = variables[2]

    # plot top xGI breakdown by xA and xG
    df_1 = PL_data_season_filter
    df_1 = df_1.sort_values(by=[x2], ascending=False).head(N)
    filepath=f"Top {N} Players by {sort_name}"
    hbarplot_players_colours_hatch(df_1,x3,x2, y, x2_title, "", f"Top {N} players by {sort_name}",
                             gameweekrange=gameweek_range, positions=positions,filepath=filepath)
def player_scatter(df, variables, season, x1_text, x2_text, gameweek_range, q,marker_size=False):
    # Sum over mins per name and per season
    variables_p90 = [x + " per 90" for x in variables]
    columns = ["Name", "Season", "Gameweek", "Position", "Mins", "Colours"]
    PL_data_all = df[columns + variables]
    PL_data_all_sum = PL_data_all.groupby(["Name", "Season", "Position", "Colours"]).sum().reset_index()
    for x in variables:
        PL_data_all_sum[f"{x} per 90"] = PL_data_all_sum[x] * 90 / PL_data_all_sum["Mins"]
    PL_data_all_sum = PL_data_all_sum[PL_data_all_sum["Mins"] > 1600]

    # Filter by current season
    PL_data_season = df[df["Season"] == season]

    # Filter data by GW range
    A = gameweek_range[0]
    B = gameweek_range[1]
    PL_data_season_filter = PL_data_season[(PL_data_season['Gameweek'] >= A) & (PL_data_season['Gameweek'] <= B)]

    # Agg over sum or mean
    method = "sum"
    if method == "mean":
        PL_data_season = PL_data_season_filter.groupby(
            ["Season", "Name", "Team", "Position", "Colours"]).mean().reset_index()
    elif method == "sum":
        PL_data_season = PL_data_season_filter.groupby(
            ["Season", "Name", "Team", "Position", "Colours"]).sum().reset_index()

    # Add per 90 stats
    for x in variables:
        PL_data_season[f"{x} per 90"] = PL_data_season[x] * 90 / PL_data_season["Mins"]
    PL_data_season = PL_data_season[PL_data_season["Mins"] > ((B + 1) - A) * 90 * 0.40]

    # Graph Inputs
    x1 = variables_p90[0]
    x2 = variables_p90[1]
    if marker_size:
        x3=variables_p90[2]
    else:
        pass

    y = "Name"

    # x v y scatter
    positions = ["Defender", "Midfielder", "Forward"]
    for position in positions:
        threshold1 = PL_data_season[PL_data_season["Position"] == position][x1].quantile(1 - q)
        threshold2 = PL_data_season[PL_data_season["Position"] == position][x2].quantile(1 - q)
        print(position, threshold1, threshold2)
        Top_Performers_Historical_x1 = PL_data_all_sum[
            (PL_data_all_sum["Position"] == position) & (PL_data_all_sum["Season"] != season)].sort_values(x1,
                                                                                                           ascending=False).head(
            2)
        Top_Performers_Historical_x1["Name"] = Top_Performers_Historical_x1["Name"] + ", " + \
                                               Top_Performers_Historical_x1["Season"].astype(str)
        Top_Performers_Historical_x2 = PL_data_all_sum[
            (PL_data_all_sum["Position"] == position) & (PL_data_all_sum["Season"] != season)].sort_values(x2,
                                                                                                           ascending=False).head(
            2)
        Top_Performers_Historical_x2["Name"] = Top_Performers_Historical_x2["Name"] + ", " + \
                                               Top_Performers_Historical_x2["Season"].astype(str)
        PL_data_season = PL_data_season.append(Top_Performers_Historical_x1)
        PL_data_season = PL_data_season.append(Top_Performers_Historical_x2)
        df_1 = PL_data_season[(PL_data_season[x1] >= threshold1) & (PL_data_season["Position"] == position) | (
                    PL_data_season[x2] >= threshold2) & (PL_data_season["Position"] == position)]
        plottitle = f"Top {int((q) * 100)}% of performers, at least {int(((B + 1) - A) * 90 * 0.5)} mins played"
        if marker_size:
            create_expected_player_graph_size(df_1, x1, x2, y, x1_text, x2_text, position, plottitle,
                                     gameweekrange=gameweek_range,marker_size=x3)
        else:
            create_expected_player_graph(df_1, x1, x2, y, x1_text, x2_text, position, plottitle,
                                              gameweekrange=gameweek_range)


