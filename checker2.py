from chart_functions import create_expected_player_graph, hbarplot_players,stacked_hbarplot_players, cumm_calc_gw,namescleaner, top_performers_name
from constants import features, teams,DATADir
import pandas as pd

# Import data
df=pd.read_csv(DATADir)
df=df.rename(columns={"GW ID":"Gameweek"})
df=df.merge(teams,on=["Team"])

#Sum over mins per name and per season
df_sum=df.groupby(["Name", "Season","Team","Colours"]).sum().reset_index()
variables=["Passes Final Third","Chances Created"]
variables_p90=[x+" per 90" for x in variables]
columns=["Name","Season","Gameweek","Position","Mins","Colours"]
PL_data_all=df[columns+variables]
PL_data_all_sum=PL_data_all.groupby(["Name", "Season","Position","Colours"]).sum().reset_index()
for x in variables:
    PL_data_all_sum[f"{x} per 90"]=PL_data_all_sum[x]*90/PL_data_all_sum["Mins"]
PL_data_all_sum=PL_data_all_sum[PL_data_all_sum["Mins"]>1600]

#Filter by current season
season=2020
PL_data_season=df[df["Season"]==season]

#Filter data by GW range
gameweek_range = [1, 38]
A = gameweek_range[0]
B = gameweek_range[1]
PL_data_season_filter=PL_data_season[(PL_data_season['Gameweek'] >= A) & (PL_data_season['Gameweek'] <= B)]

# Agg over sum or mean
method = "sum"
if method == "mean":
    PL_data_season = PL_data_season_filter.groupby(["Season","Name", "Team", "Position", "Colours"]).mean().reset_index()
elif method == "sum":
    PL_data_season = PL_data_season_filter.groupby(["Season","Name", "Team", "Position", "Colours"]).sum().reset_index()

#Add per 90 stats
for x in variables:
    PL_data_season[f"{x} per 90"]=PL_data_season[x]*90/PL_data_season["Mins"]
PL_data_season=PL_data_season[PL_data_season["Mins"]>(B-A)*90*0.5]

#Graph Inputs
x1 = "Passes Final Third per 90"
x2 = "Chances Created per 90"
y = "Name"
x1_text="Final Third Passes per 90"
x2_text="Chances Created per 90"
gameweeks=gameweek_range[1]-gameweek_range[0]
q=0.25
threshold1=PL_data_season[x1].quantile(q)
threshold2=PL_data_season[x2].quantile(q)

# x v y scatter
positions=["Defender","Midfielder","Forward"]
for position in positions:
    threshold1=PL_data_season[PL_data_season["Position"]==position][x1].quantile(q)
    threshold2=PL_data_season[PL_data_season["Position"]==position][x2].quantile(q)
    print(position,threshold1,threshold2)
    Top_Performers_Historical_x1=PL_data_all_sum[(PL_data_all_sum["Position"]==position)&(PL_data_all_sum["Season"]!=season)].sort_values(x1,ascending=False).head(2)
    Top_Performers_Historical_x1["Name"]=Top_Performers_Historical_x1["Name"]+", "+Top_Performers_Historical_x1["Season"].astype(str)
    Top_Performers_Historical_x2=PL_data_all_sum[(PL_data_all_sum["Position"]==position)&(PL_data_all_sum["Season"]!=season)].sort_values(x2,ascending=False).head(2)
    Top_Performers_Historical_x2["Name"]=Top_Performers_Historical_x2["Name"]+", "+Top_Performers_Historical_x2["Season"].astype(str)
    PL_data_season=PL_data_season.append(Top_Performers_Historical_x1)
    PL_data_season=PL_data_season.append(Top_Performers_Historical_x2)
    df_1 = PL_data_season[(PL_data_season[x1] >= threshold1) & (PL_data_season["Position"] == position)&(PL_data_season[x2] >= threshold2)]
    create_expected_player_graph(df_1, x1, x2, y, x1_text, x2_text, f"Premier League {season}-{season+1}\n{x1_text} vs {x2_text}: f{position}s\nTop {int((1-q)*100)}% of performers \nAt least {((B-A)*90*0.5)} mins played",
                                 gameweekrange=gameweek_range)

