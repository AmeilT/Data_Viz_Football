from functions.Viz_Chart_Functions import import_data
from functions.Viz_Combine_Charts import player_scatter, hbar_player, hbar_player_hatch

season = 2021
gameweek = 15
gameweek_range = [gameweek - 4,gameweek]

# Import and process data
df = import_data()

# PLAYER
# xG vs xA
player_scatter(df=df, variables=["GoalsxG", "AssistsxA", "Attempts"], season=season, x1_text="Expected Goals per 90",
             x2_text="Expected Assists per 90", gameweek_range=gameweek_range, q=0.3, marker_size=False)

# # G vs xG
hbar_player(df, ["GoalsG", "GoalsxG"], season, gameweek_range=gameweek_range, sort="GoalsΔ", x1_title="Goals Scored",
            x2_title="Expected Goals Scored", y="Name", N=15, sort_name="xG")

# # # GI vs xGI
hbar_player_hatch(df, ["InvolvementGI", "InvolvementxGI", "AssistsxA"], season, gameweek_range=gameweek_range,
                  sort="InvolvementΔ", x1_title="Goal Involvement", x2_title="Expected Goal Involvement", y="Name",
                  N=15, sort_name="xGI")
hbar_player(df, ["InvolvementGI", "InvolvementxGI"], season, gameweek_range=gameweek_range, sort="InvolvementΔ",
             x1_title="Goal Involvement", x2_title="Expected Goal Involvement", y="Name", N=15, sort_name="xGI")

#     #Attempts vs Attempts in Box
player_scatter(df=df, variables=["npxG", "Attempts In Box"], season=season, x1_text="Non Penalty xG per 90",
               x2_text="Attempts In Box per 90", gameweek_range=gameweek_range, q=0.30)
player_scatter(df=df, variables=["Attempts On Target", "Attempts In Box"], season=season, x1_text="Attempts On Target per 90",
               x2_text="Attempts In Box per 90", gameweek_range=gameweek_range, q=0.3, marker_size=False)

# Chances Created
player_scatter(df=df, variables=["Chances Created", "AssistsxA", "Attempts"], season=season,
               x1_text="Chances Created per 90", x2_text="Expected Assists per 90", gameweek_range=gameweek_range,
               q=0.3, marker_size=False)
player_scatter(df=df, variables=["Chances Created", "Attempts In Box"], season=season,
               x1_text="Chances Created per 90", x2_text="Attempts in Box per 90", gameweek_range=gameweek_range,
               q=0.3, marker_size=False)
hbar_player(df, ["Assists", "Chances Created"], season, gameweek_range=gameweek_range, sort="DeltaAssists",
            x1_title="Assists", x2_title="Chances Created", y="Name", N=15, sort_name="Chances Created")

#Involvement
player_scatter(df=df, variables=['Passes ReceivedFin 3rd', 'TouchesFin 3rd'], season=season,
               x1_text="Passes Received. Fin.3rd per 90", x2_text="Touches inFin.3rd per 90",
               gameweek_range=gameweek_range, q=0.3, marker_size=False)

#TEAM
