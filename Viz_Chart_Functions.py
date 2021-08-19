import matplotlib.pyplot as plt
import numpy as np
from adjustText import adjust_text
import re
import seaborn as sns
import networkx as nx
from data_viz_constants import title_font, title_size, label_font, label_size, text_colour, back_colour, y_equals_x
from constants import positions,pos_colours,path
import matplotlib.patches as patches
import pandas as pd

def hex_to_rgb(hx, hsl=True):
    """Converts a HEX code into RGB or HSL.
    Args:
        hx (str): Takes both short as well as long HEX codes.
        hsl (bool): Converts the given HEX code into HSL value if True.
    Return:
        Tuple of length 3 consisting of either int or float values."""
    if re.compile(r'#[a-fA-F0-9]{3}(?:[a-fA-F0-9]{3})?$').match(hx):
        div = 255.0 if hsl else 0
        if len(hx) <= 4:
            return tuple(int(hx[i] * 2, 16) / div if div else
                         int(hx[i] * 2, 16) for i in (1, 2, 3))
        else:
            return tuple(int(hx[i:i + 2], 16) / div if div else
                         int(hx[i:i + 2], 16) for i in (1, 3, 5))
    else:
        raise ValueError(f'"{hx}" is not a valid HEX code.')

def create_expected_player_graph(data, x1, x2, y, xtitle, ytitle,position, plottitle, gameweekrange):
    # Create Figure (empty canvas)
    fig, axes = plt.subplots()
    #plt.rcParams["text.usetex"] = True
    #rc('text.latex', preamble=r'\usepackage[cm]{sfmath}')
    axes.grid(False)
    # colours
    plt.rcParams['figure.facecolor'] = back_colour
    axes.set_facecolor(back_colour)
    fig.patch.set_facecolor(back_colour)
    axes.spines['left'].set_color(text_colour)
    axes.spines['bottom'].set_color(text_colour)
    axes.spines['top'].set_visible(False)
    axes.tick_params(axis='x', colors=text_colour)
    axes.tick_params(axis='y', colors=text_colour)
    season=data["Season"].mode().iloc[0]


    #Titles
    shift=0.03
    plt.figtext(0.1,0.97,f"Premier League {season}-{season+1}",color="w",size=15)
    plt.figtext(0.1,1-shift*1.8,f"{position}s",color="w",size=12)
    plt.figtext(0.1,1-shift*2.5,f"Gameweeks {gameweekrange[0]} to {gameweekrange[1]}",color="w",size=12)
    plt.figtext(0.1,1-shift*3.3,plottitle,color="w",size=12)

    # Plot on that set of axes
    axes.scatter(data[x1], data[x2])
    axes.set_xlabel(xtitle, color=text_colour,family = 'sans-serif')  # Notice the use of set_ to begin methods
    axes.set_ylabel(ytitle, color=text_colour,family = 'sans-serif')


    #Make any top performers transparent
    # Label Points
    season = data["Season"].mode()[0]
    texts = []
    for x, y, s, n in zip(data[x1], data[x2], data["Name"], data["Season"]):
        if (n == season) == False:
            texts.append(
                plt.text(x, y, s, color=text_colour,
                         fontsize=label_size, fontstyle="italic", alpha=0.6, va="center"))
        else:
            texts.append(
                plt.text(x, y, s, color=text_colour,
                         fontsize=label_size, va="center"))
    adjust_text(texts, arrowprops=dict(arrowstyle='-', color='w', connectionstyle="angle3,angleA=0,angleB=-90",
                                       relpos=(0.5, 0.5)))

    for i in np.arange(0, data.shape[0]):
        plt.plot(data[x1].iloc[i], data[x2].iloc[i], color="#020530", markeredgecolor=data["Colours"].iloc[i],
                 markeredgewidth=2, marker="o")
        # text boxes
        facecolor = "w"
    if x1 == "xG Expected GoalsG":
        axes.text(0.4, 2, 'Unlucky teams', style='italic',
                  bbox={'facecolor': facecolor, 'alpha': 0.3, 'pad': 10})

        axes.text(1.9, 0.5, 'Lucky teams', style='italic',
                  bbox={'facecolor': facecolor, 'alpha': 0.3, 'pad': 10})
    elif x2 == "xG Expected GoalsG":
        axes.text(0.4, 2, 'Lucky teams', style='italic',
                  bbox={'facecolor': facecolor, 'alpha': 0.3, 'pad': 10})

        axes.text(1.9, 0.5, 'Unlucky teams', style='italic',
                  bbox={'facecolor': facecolor, 'alpha': 0.3, 'pad': 10})
    else:
        pass


def hbarplot(data, x1, x2, y, ytitle, xtitle, plottitle, gameweekrange,filepath):
    sns.set_theme(style="whitegrid")

    # Initialize the matplotlib figure
    fig, axes = plt.subplots(figsize=(18, 15))

    # colours
    backcolour = "#020530"
    titlecolor = "w"

    # Axes
    plt.rcParams['figure.facecolor'] = backcolour
    axes.set_facecolor(backcolour)
    fig.patch.set_facecolor(backcolour)
    axes.set_xlabel(xtitle, color=titlecolor)  # Notice the use of set_ to begin methods
    axes.set_ylabel(y, color=titlecolor)
    axes.spines['bottom'].set_color(backcolour)
    axes.spines['top'].set_color(backcolour)
    axes.xaxis.label.set_color(titlecolor)
    axes.tick_params(axis='x', colors=titlecolor)
    axes.yaxis.label.set_color(titlecolor)
    axes.tick_params(axis='y', colors=titlecolor)

    if gameweekrange == "ALL":
        axes.set_title(f"{plottitle}\n 21/22 Season so far", color="w",
                       loc="left", size=title_size, font=title_font)
    elif gameweekrange[0] == gameweekrange[1]:
        axes.set_title(f"{plottitle}\nGameweek {gameweekrange[0]}", color="w", loc="left",
                       size=title_size, font=title_font)
    else:
        axes.set_title(f"{plottitle}\nbetween gameweek {gameweekrange[0]} and {gameweekrange[1]}", color="w",
                       loc="left", size=title_size, font=title_font)

    # Plot 1
    sns.set_color_codes("pastel")
    sns.barplot(x=data[x1], y=y, data=data,
                label="Goals Scored", color="r", alpha=0.8, order=data.sort_values(x1, ascending=False)[y])

    # Plot 2
    sns.set_color_codes("muted")
    sns.barplot(x=data[x2], y=y, data=data,
                label="Expected Goals", color="b", alpha=0.5, order=data.sort_values(x1, ascending=False)[y])

    # Add a legend and informative axis label
    axes.legend(ncol=2, loc="lower right", frameon=True)
    axes.set(ylabel=ytitle, xlabel=xtitle)
    sns.despine(left=True, bottom=True)
    fig.savefig(filepath,bbox_inches='tight')

def hbarplot_players(data, x1, x2, y, x1title,x2title,ytitle, plottitle, gameweekrange,filepath):
    sns.set_theme(style="whitegrid")

    # Initialize the matplotlib figure
    fig, axes = plt.subplots(figsize=(6, 15))

    # colours
    backcolour = "#020530"
    titlecolor = "w"

    # Axes
    plt.rcParams['figure.facecolor'] = backcolour
    axes.set_facecolor(backcolour)
    fig.patch.set_facecolor(backcolour)
    axes.set_xlabel(x1title, color=titlecolor)  # Notice the use of set_ to begin methods
    axes.set_ylabel(y, color=titlecolor)
    axes.spines['bottom'].set_color(backcolour)
    axes.spines['top'].set_color(backcolour)
    axes.xaxis.label.set_color(titlecolor)
    axes.tick_params(axis='x', colors=titlecolor)
    axes.yaxis.label.set_color(titlecolor)
    axes.tick_params(axis='y', colors=titlecolor)

    if gameweekrange == "ALL":
        axes.set_title(f"{plottitle}\n 21/22 Season so far", color="w",
                       loc="left", size=title_size, font=title_font)
    elif gameweekrange[0] == gameweekrange[1]:
        axes.set_title(f"{plottitle}\nGameweek {gameweekrange[0]}", color="w", loc="left",
                       size=title_size, font=title_font)
    else:
        axes.set_title(f"{plottitle}\nbetween gameweek {gameweekrange[0]} and {gameweekrange[1]}", color="w",
                       loc="left", size=title_size, font=title_font)

    # Plot 1
    sns.set_color_codes("pastel")
    sns.barplot(x=data[x1], y=y, data=data,
                label=x1title, color="r", alpha=0.8)

    # Plot 2
    sns.set_color_codes("muted")
    sns.barplot(x=data[x2], y=y, data=data,
                label=x2title, color="b", alpha=0.5)

    # Add a legend and informative axis label
    axes.legend(ncol=2, loc="lower right", frameon=True)
    axes.set(ylabel=ytitle,xlabel=x2title)
    sns.despine(left=True, bottom=True)

    fig.savefig(filepath)

def hbarplot_players_colours(data, x1, y, x1title,ytitle, plottitle, gameweekrange,positions=positions,pos_colours=pos_colours,N=15,filepath=path):
    sns.set_theme(style="whitegrid")

    # Initialize the matplotlib figure
    fig, axes = plt.subplots(figsize=(6, 15))

    # colours
    backcolour = "#020530"
    titlecolor = "w"

    # Axes
    plt.rcParams['figure.facecolor'] = backcolour
    axes.set_facecolor(backcolour)
    fig.patch.set_facecolor(backcolour)
    axes.set_xlabel(x1title, color=titlecolor)  # Notice the use of set_ to begin methods
    axes.set_ylabel(y, color=titlecolor)
    axes.spines['bottom'].set_color(backcolour)
    axes.spines['top'].set_color(backcolour)
    axes.xaxis.label.set_color(titlecolor)
    axes.tick_params(axis='x', colors=titlecolor)
    axes.yaxis.label.set_color(titlecolor)
    axes.tick_params(axis='y', colors=titlecolor)

    if gameweekrange == "ALL":
        axes.set_title(f"{plottitle}\n 21/22 Season so far", color="w",
                       loc="left", size=title_size, font=title_font)
    elif gameweekrange[0] == gameweekrange[1]:
        axes.set_title(f"{plottitle}\nGameweek {gameweekrange[0]}", color="w", loc="left",
                       size=title_size, font=title_font)
    else:
        axes.set_title(f"{plottitle}\nbetween gameweek {gameweekrange[0]} and {gameweekrange[1]}", color="w",
                       loc="left", size=title_size, font=title_font)
    #data=data.merge(positions,on=["Position"])

    # Plot 1
    top_xg=data.sort_values(x1,ascending=False).head(N)
    sns.set_color_codes("pastel")
    for position,colour in list(zip(positions,pos_colours)):
        sns.barplot(x=top_xg[top_xg["Position"]==position][x1], y=y, data=data,
                    label=position, color=colour, alpha=0.8)



    # Add a legend and informative axis label
    axes.legend(ncol=2, loc="lower right", frameon=True)
    axes.set(ylabel=ytitle,xlabel=x1title)
    sns.despine(left=True, bottom=True)
    fig.savefig(filepath)

def hbarplot_players_colours_hatch(data, x3,x2, y, x1title,ytitle, plottitle, gameweekrange,positions=positions,pos_colours=pos_colours,N=15,filepath=path):
    sns.set_theme(style="whitegrid")

    # Initialize the matplotlib figure
    fig, axes = plt.subplots(figsize=(6, 15))

    # colours
    backcolour = "#020530"
    titlecolor = "w"

    # Axes
    plt.rcParams['figure.facecolor'] = backcolour
    axes.set_facecolor(backcolour)
    fig.patch.set_facecolor(backcolour)
    axes.set_xlabel(x1title, color=titlecolor)  # Notice the use of set_ to begin methods
    axes.set_ylabel(y, color=titlecolor)
    axes.spines['bottom'].set_color(backcolour)
    axes.spines['top'].set_color(backcolour)
    axes.xaxis.label.set_color(titlecolor)
    axes.tick_params(axis='x', colors=titlecolor)
    axes.yaxis.label.set_color(titlecolor)
    axes.tick_params(axis='y', colors=titlecolor)

    if gameweekrange == "ALL":
        axes.set_title(f"{plottitle}\n 21/22 Season so far", color="w",
                       loc="left", size=title_size, font=title_font)
    elif gameweekrange[0] == gameweekrange[1]:
        axes.set_title(f"{plottitle}\nGameweek {gameweekrange[0]}", color="w", loc="left",
                       size=title_size, font=title_font)
    else:
        axes.set_title(f"{plottitle}\nbetween gameweek {gameweekrange[0]} and {gameweekrange[1]}", color="w",
                       loc="left", size=title_size, font=title_font)

    # Plot 1
    top_xg=data.sort_values(x2,ascending=False).head(N)
    sns.set_color_codes("pastel")
    for position,colour in list(zip(positions,pos_colours)):
        bar1=sns.barplot(x=top_xg[top_xg["Position"]==position][x2], y=y, data=data,
                    label=position, color=colour, alpha=0.8)
        if position==positions[0]:
            sns.barplot(x=top_xg[top_xg["Position"] == position][x3], y=y, data=data,
                    label="xAssists", color=colour, alpha=0.8,hatch="xx")
        else:
            sns.barplot(x=top_xg[top_xg["Position"] == position][x3], y=y, data=data,
                        label="", color=colour, alpha=0.8, hatch="xx")


    # Add a legend and informative axis label
    axes.legend(ncol=2, loc="lower right", frameon=True)
    axes.set(ylabel=ytitle,xlabel=x1title)
    sns.despine(left=True, bottom=True)
    rect1 = patches.Rectangle((0,0),1,1,facecolor=pos_colours[0])
    rect2 = patches.Rectangle((0,0),1,1,facecolor=pos_colours[1])
    rect3 = patches.Rectangle((0,0),1,1,facecolor=pos_colours[2])
    rect4 = patches.Rectangle((0,0),1,1,facecolor="black",hatch="xx")
    rects=[rect1,rect2,rect3,rect4]
    positions.append("xAssists")
    axes.legend(rects, positions)
    fig.savefig(filepath)

def stacked_hbarplot_players(data,y, xtitle, plottitle, gameweekrange,filepath):
    sns.set_theme(style="whitegrid")

    # Initialize the matplotlib figure
    fig, axes = plt.subplots()

    # colours
    backcolour = "#020530"
    titlecolor = "w"

    # Axes
    plt.rcParams['figure.facecolor'] = backcolour
    axes.set_facecolor(backcolour)
    fig.patch.set_facecolor(backcolour)
    axes.set_xlabel(xtitle, color=titlecolor)  # Notice the use of set_ to begin methods
    #axes.set_ylabel(y, color=titlecolor)
    axes.spines['bottom'].set_color(backcolour)
    axes.spines['top'].set_color(backcolour)
    axes.xaxis.label.set_color(titlecolor)
    axes.tick_params(axis='x', colors=titlecolor)
    axes.yaxis.label.set_color(titlecolor)
    axes.tick_params(axis='y', colors=titlecolor)

    if gameweekrange == "ALL":
        axes.set_title(f"{plottitle}\n 21/22 Season so far", color="w",
                       loc="left", size=title_size, font=title_font)
    elif gameweekrange[0] == gameweekrange[1]:
        axes.set_title(f"{plottitle}\nGameweek {gameweekrange[0]}", color="w", loc="left",
                       size=title_size, font=title_font)
    else:
        axes.set_title(f"{plottitle}\nbetween gameweek {gameweekrange[0]} and {gameweekrange[1]}", color="w",
                       loc="left", size=title_size, font=title_font)
    #alpha = 1
    colours=["b","g","r","m","c"]
    a=list(zip(range(gameweekrange[0],gameweekrange[1]+1),colours))
    for x,colour in a:
        # Plot
        gw_list = range(gameweekrange[0],gameweekrange[1]+1)
        sns.set_color_codes("pastel")
        sns.barplot(x=data[f"Cummulative GW {x}"], y=y,data=data,
                    label=f"Gameweek {x}", color=colour,zorder=len(gw_list)-gw_list.index(x))
        plt.xlabel(xtitle)
        plt.ylabel("")

        #alpha-=0.33

    # Put a legend below current axis
    axes.legend(loc='upper center', bbox_to_anchor=(0.5, -0.09),
              fancybox=True, shadow=True, ncol=len(gw_list))

    axes.set(xlabel=xtitle)
    sns.despine(left=True, bottom=True)
    fig.savefig(filepath)

def stacked_hbarplot_players_grid(PL_data_season_filter,gameweek_range,N,sort_name,positions,filepath,x2,x2_title):
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
            filepath = f"{x2},Top {N} Player by {sort_name} by Gameweek"
            gw_list = range(gameweek_range[0],gameweek_range[1]+1)
            sns.set_color_codes("pastel")
            test=test.sort_values(f"Cummulative GW {x}",ascending=True)
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

    fig.supxlabel(f"{x2_title}",color=titlecolor)
    plt.rcParams['figure.facecolor'] = backcolour


    # Put a legend below current axis

    #axes.legend(loc='upper center', bbox_to_anchor=(0.5, -0.09),
              #fancybox=True, shadow=True, ncol=len(gw_list))

    #axes.set(xlabel="xtitle")
    sns.despine(left=True, bottom=True)
    fig.savefig(filepath)

def namescleaner(x):
    for y in ["van ", "Van ", "de", "De", "el", "El","C"]:
        if y in x.split():
            return x
        else:
            pass
    if len(x.split())==1:
        return x
    else:
        return x.split()[1]

def cumm_calc_gw(df,gw_list,N):
    for gw in gw_list:
        cumm_list = gw_list[:gw_list.index(gw) + 1]
        df[f"Cummulative GW {gw}"] = df[cumm_list].sum(axis=1)
    df = df.reset_index().sort_values(f"Cummulative GW {gw_list[-1]}", ascending=False).head(N)
    return df

def top_performers_name(df):
    season=df["Season"]
    name=df["Name"]
    return f"{name},{season}"

def repel_labels(ax, x, y, labels, k=0.01):
    G = nx.DiGraph()
    data_nodes = []
    init_pos = {}
    for xi, yi, label in zip(x, y, labels):
        data_str = 'data_{0}'.format(label)
        G.add_node(data_str)
        G.add_node(label)
        G.add_edge(label, data_str)
        data_nodes.append(data_str)
        init_pos[data_str] = (xi, yi)
        init_pos[label] = (xi, yi)

    pos = nx.spring_layout(G, pos=init_pos, fixed=data_nodes, k=k)

    # undo spring_layout's rescaling
    pos_after = np.vstack([pos[d] for d in data_nodes])
    pos_before = np.vstack([init_pos[d] for d in data_nodes])
    scale, shift_x = np.polyfit(pos_after[:,0], pos_before[:,0], 1)
    scale, shift_y = np.polyfit(pos_after[:,1], pos_before[:,1], 1)
    shift = np.array([shift_x, shift_y])
    for key, val in pos.items():
        pos[key] = (val*scale) + shift

    for label, data_str in G.edges():
        ax.annotate(label[0],
                    xy=pos[data_str], xycoords='data',
                    xytext=pos[label], textcoords='data',color="w",
                    arrowprops=dict(arrowstyle="-",
                                    shrinkA=0, shrinkB=0,
                                    connectionstyle="arc3",
                                    color='w'), )
        print(label)
    # expand limits
    all_pos = np.vstack(pos.values())
    x_span, y_span = np.ptp(all_pos, axis=0)
    mins = np.min(all_pos-x_span*0.15, 0)
    maxs = np.max(all_pos+y_span*0.15, 0)
    ax.set_xlim([mins[0], maxs[0]])
    ax.set_ylim([mins[1], maxs[1]])

