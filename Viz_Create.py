from Viz_Combine_Charts import player_scatter, hbar_player,hbar_player_hatch
from constants import teams, DATADir,path
from Viz_Chart_Functions import namescleaner
import pandas as pd

season = 2021
gameweek_range = [1, 1]
# Import data
df = pd.read_csv(DATADir)
df = df.rename(columns={"GW ID": "Gameweek"})
df = df.merge(teams, on=["Team"])
df["Name"] = df["Name"].apply(namescleaner)
df["InvolvementGI"]=df["Goals"]=df["Assists"]
df["Attempts"]=90/df["AttemptsM/C"]

# PLAYER
    # xG vs xA
#player_scatter(df=df,variables=["GoalsxG","AssistsxA"],season=season,x1_text="Expected Goals per 90",x2_text="Expected Assists per 90",gameweek_range=gameweek_range,q=0.3)
    # G vs xG
hbar_player(df,["GoalsG","GoalsxG"],season,gameweek_range=[1,1],sort="GoalsΔ",x1_title="Goals Scored",x2_title="Expected Goals Scored",y="Name",N=15,sort_name="xG")
    # GI vs xGI
#hbar_player_hatch(df,["InvolvementGI","InvolvementxGI","AssistsxA"],season,gameweek_range=[1,1],sort="InvolvementΔ",x1_title="Goal Involvement",x2_title="Expected Goal Involvement",y="Name",N=15,sort_name="xGI")
#hbar_player(df,["InvolvementGI","InvolvementxGI"],season,gameweek_range=[1,1],sort="InvolvementΔ",x1_title="Goal Involvement",x2_title="Expected Goal Involvement",y="Name",N=15,sort_name="xGI")
    #Attempts vs Attempts in Box
#player_scatter(df=df,variables=["Attempts","Attempts In Box"],season=season,x1_text="Attempts per 90",x2_text="Attempts In Box per 90",gameweek_range=gameweek_range,q=0.3)
#player_scatter(df=df,variables=["GoalsxG","Attempts"],season=season,x1_text="xG per 90",x2_text="Attempts per 90",gameweek_range=gameweek_range,q=0.3)


# TEAM
