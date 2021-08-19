from Viz_Chart_Functions import *
from data_viz_constants import *
from constants import *
import os
os.chdir(path)
import pandas as pd


variables=["GoalsG","GoalsxG"]
N=15
sort="GoalsΔ"
x1_title="Goals Scored"
x2_title="Expected Goals Scored"
y="Name"
sort_name="xG"


season = 2021
gameweek_range = [1, 1]
# Import data
df = pd.read_csv(DATADir)
df = df.rename(columns={"GW ID": "Gameweek"})
df = df.merge(teams, on=["Team"])
df["Name"] = df["Name"].apply(namescleaner)
df["InvolvementGI"]=df["Goals"]=df["Assists"]
df["Attempts"]=90/df["AttemptsM/C"]

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

# plot top X overacheivers
filepath=f"{x1}_{x2},Top {N} overperformers by {sort_name}"
df_1 = PL_data_season_filter[(PL_data_season_filter[x1] >= 1)]
df_1 = df_1.sort_values(by=[sort], ascending=False).head(N)
hbarplot_players(df_1, x1, x2, y, x1_title, x2_title, "", f"Top {N} overperformers by {sort_name}",
                 gameweekrange=gameweek_range,filepath=filepath)

# plot top X underacheivers
filepath=f"{x1}_{x2},Top {N} underperformers by {sort_name}"
df_1 = PL_data_season_filter[(PL_data_season_filter[x2]) > 0.1]
df_1 = df_1.sort_values(by=[sort], ascending=True).head(N)
hbarplot_players(df_1, x1, x2, y, x1_title, x2_title, "", f"Top {N} underperformers by {sort_name}",
                 gameweekrange=gameweek_range,filepath=filepath)
# plot top xGI
filepath=f"{x1}_{x2},Top {N} players by {sort_name}"
df_1 = PL_data_season_filter
df_1 = df_1.sort_values(by=[x2], ascending=False).head(N)

hbarplot_players_colours(df_1, x2, y, x2_title, "", f"Top {N} players by {sort_name}",
                         gameweekrange=gameweek_range, positions=positions,filepath=filepath)

def stacked_hbarplot_players_grid(N,sort_name,df_stacked,positions,filepath,x2,x2_title):
    # Plot stacked xG by Gameweek
    plottitle=f"Top {N} players by {sort_name} by Gameweek"


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
    positions.append("r")
    for i,position in enumerate(positions[::-1]):
        for x,colour in a:
            # Plot
            df_stacked = PL_data_season_filter[["Name", "Gameweek", x2, "Position"]]
            df_stacked = df_stacked[df_stacked["Position"].str.contains(position)]
            test = pd.pivot_table(df_stacked, index='Name', values=x2, columns='Gameweek')
            gw_list = range(gameweek_range[0],gameweek_range[1]+1)
            test = cumm_calc_gw(test, gw_list, N)
            filepath = f"{x1}_{x2},Top {N} Player by {sort_name} by Gameweek"
            gw_list = range(gameweek_range[0],gameweek_range[1]+1)
            sns.set_color_codes("pastel")
            test=test.sort_values(f"Cummulative GW {x}",ascending=True)

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

    fig.supxlabel(f"{x2_title}",color=titlecolor)
    plt.rcParams['figure.facecolor'] = backcolour


    # Put a legend below current axis

    #axes.legend(loc='upper center', bbox_to_anchor=(0.5, -0.09),
              #fancybox=True, shadow=True, ncol=len(gw_list))

    #axes.set(xlabel="xtitle")
    sns.despine(left=True, bottom=True)
    fig.savefig(filepath)