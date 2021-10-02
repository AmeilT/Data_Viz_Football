from Viz_Combine_Charts import *
from constants import teams, DATADir,path,positions
from Viz_Chart_Functions import *

import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sns

season = 2021
gameweek_range = [1, 2]
# Import data
df = pd.read_csv(DATADir)
df = df.rename(columns={"GW ID": "Gameweek"})
df = df.merge(teams, on=["Team"])
df["Name"] = df["Name"].apply(namescleaner)
df["InvolvementGI"]=df["GoalsG"]+df["AssistsA"]
df["Attempts"]=90/df["AttemptsM/C"]
df["Attempts"]=[0 if math.isinf(x) else x for x in df["Attempts"]]

variables=["InvolvementGI","InvolvementxGI"]
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

x2="GoalsxG"
sort_name="GoalsxG"
season = 2021
N=15
# Plot stacked xG by Gameweek
plottitle=f"Top players by  by Gameweek"

# Initialize the matplotlib figure
nrows=2
ncolumns=2
fig, axes = plt.subplots(nrows,ncolumns,sharex=True)
axes = axes.flatten()
sns.set_theme(style="whitegrid")

# colours
backcolour = "#020530"
titlecolor = "w"

colours=["b","g","r","m","c"]
a=list(zip(range(gameweek_range[0],gameweek_range[1]+1),colours))
b=positions + ["r"]
for i,position in enumerate(b[::-1]):
    for x,colour in a:
        # Plot
        df_stacked = PL_data_season_filter[["Name", "Gameweek", x2, "Position"]]
        df_stacked = df_stacked[df_stacked["Position"].str.contains(position)]
        test = pd.pivot_table(df_stacked, index='Name', values=x2, columns='Gameweek')
        gw_list = range(gameweek_range[0],gameweek_range[1]+1)
        test = cumm_calc_gw(test, gw_list, N)
        filepath = f"{x2},Top {N} Player by {sort_name} by Gameweek"
        gw_list = range(gameweek_range[0],gameweek_range[1]+1)
        sns.set_color_codes("pastel")
        test=test.sort_values(f"Cummulative GW {gameweek_range[-1]}",ascending=True)
        y="Name"
        axes[i].barh(width=test[f"Cummulative GW {x}"], y=y,data=test,label=f"Gameweek {x}", color=colour,zorder=len(gw_list)-gw_list.index(x))
        #Axes of Subplot
        axes[i].set_ylabel("", color=titlecolor)
        axes[i].tick_params(axis='y', colors=titlecolor)
        axes[i].tick_params(axis='x', colors=titlecolor)
        axes[i].set_facecolor(backcolour)
        fig.patch.set_facecolor(backcolour)
        plt.xlabel("xtitle")
        axes[i].grid(False)
        axes[i].xaxis.grid()  # vertical lines
        axes[i].set_title(f"{position}s", color="w",
                          loc="left", size=title_size, font=title_font)
        if position=="r":
            axes[i].set_title(f"All Players", color="w",loc = "left", size = title_size, font = title_font)

#Title
if gameweek_range == "ALL":
    fig.suptitle(f"{plottitle}\n 21/22 Season so far", color="w", size=title_size,font=title_font,x=0.1, y=0.97, horizontalalignment='left', verticalalignment='top')
elif gameweek_range[0] == gameweek_range[1]:
    fig.suptitle(f"{plottitle}\nGameweek {gameweek_range[0]}", color="w",
               size=title_size, font=title_font,x=0.1, y=0.97, horizontalalignment='left', verticalalignment='top')
else:
    fig.suptitle(f"{plottitle}\nbetween gameweek {gameweek_range[0]} and {gameweek_range[1]}", color="w", size=title_size, font=title_font,x=0.1, y=0.97, horizontalalignment='left', verticalalignment='top')

fig.supxlabel(f"ws",color=titlecolor)
plt.rcParams['figure.facecolor'] = backcolour