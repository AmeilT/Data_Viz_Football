from chart_functions import create_expected_player_graph, hbarplot_players,stacked_hbarplot_players, cumm_calc_gw,namescleaner
from constants import features, teams
import pandas as pd
import os
from pathlib import Path
import seaborn as sns

# Import data
season = 2020
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
gameweek_range = [36, 38]
A = gameweek_range[0]
B = gameweek_range[1]

for key, value in dict_data.items():
    dict_data[key] = value.loc[(value['Gameweek'] >= A) & (value['Gameweek'] <= B)]

#Merge two datasets together
data1="involvement_data"
data2="distribution_data"

df=dict_data[f"{data1}"].merge(dict_data[f"{data2}"],on=["Name","Gameweek","Team","Position","Colours"])

# Graph Inputs
method = "sum"
if method == "mean":
    df = df.groupby(["Name", "Team", "Colours"]).mean().reset_index()
elif method == "sum":
    df = df.groupby(["Name", "Team", "Position", "Colours"]).sum().reset_index()

x1 = "Final ThirdSP"
x2 = "Assist PotentialCC"
y = "Name"
x1_text="Final Third Passes"
x2_text="Chances Created"
gameweeks=gameweek_range[1]-gameweek_range[0]
# xGI vs GI graph
df_1 = df[(df[x1] >= gameweeks) & (df["Position"] == "Defender")&(df[x2] >= gameweeks)]
create_expected_player_graph(df_1, x1, x2, y, x1_text, x2_text, f"{x1_text} vs {x2_text}: Defenders\nAt least {gameweeks} {x1_text} and {gameweeks} {x2_text}",
                             gameweekrange=gameweek_range)
df_1 = df[(df[x1] > gameweeks*2) & (df["Position"] == "Midfielder")&(df[x2] > gameweeks*2)]
create_expected_player_graph(df_1, x1, x2, y, x1_text, x2_text, f"{x1_text} vs {x2_text}: Midfielders\nAt least {gameweeks} {x1_text} and {gameweeks} {x2_text}",
                             gameweekrange=gameweek_range)
df_1 = df[(df[x1] > gameweeks) & (df["Position"] == "Forward")&(df[x2] > gameweeks)]
create_expected_player_graph(df_1, x1, x2, y, x1_text, x2_text, f"{x1_text} vs {x2_text}: Forwards\nAt least {gameweeks} {x1_text} and {gameweeks} {x2_text}",
                             gameweekrange=gameweek_range)

df_1 = df[(df[x1] > gameweeks*2) & (df[x2] >gameweeks*2)]
create_expected_player_graph(df_1, x1, x2, y,x1_text, x2_text, f"{x1_text} vs {x2_text}",
                             gameweekrange=gameweek_range)

