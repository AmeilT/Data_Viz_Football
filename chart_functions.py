import matplotlib.pyplot as plt
import numpy as np
from adjustText import adjust_text
import re
import seaborn as sns

from constants import teams
from data_viz_constants import title_font, title_size, label_font, label_size, text_colour, back_colour, y_equals_x


# from highlight_text.htext import htext, fig_htext

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

def create_expected_goals_player_graph(data, x1, x2, y, xtitle, ytitle, plottitle, gameweekrange):
    # Create Figure (empty canvas)
    fig, axes = plt.subplots(constrained_layout=True)

    # Move set of axes to figure
    # axes = fig.add_axes([0, 0, 0.8, 0.8])  # left, bottom, width, height (range 0 to 1)

    # Hide grid lines
    axes.grid(False)

    # axis limits
    plt.ylim(0, max(data[x1].max()+1,data[x2].max()+1))
    plt.xlim(0, max(data[x1].max()+1,data[x2].max()+1))

    # colours
    plt.rcParams['figure.facecolor'] = back_colour
    axes.set_facecolor(back_colour)
    fig.patch.set_facecolor(back_colour)
    plt.rcParams["font.family"] = label_font
    axes.spines['left'].set_color(text_colour)
    axes.spines['bottom'].set_color(text_colour)
    axes.spines['top'].set_visible(False)
    axes.tick_params(axis='x', colors=text_colour)
    axes.tick_params(axis='y', colors=text_colour)

    if gameweekrange == "ALL":
        axes.set_title(f"{plottitle}\n 21/22 Season so far", color="w", loc="left", size=title_size, font=title_font)
    elif gameweekrange[0] == gameweekrange[1]:
        axes.set_title(f"{plottitle}\nGameweek {gameweekrange[0]}", color="w", loc="left", size=title_size,
                       font=title_font)
    else:
        axes.set_title(f"{plottitle}\nbetween gameweek {gameweekrange[0]} and {gameweekrange[1]}", color="w",
                       loc="left", size=title_size,
                       font=title_font)

    # Plot on that set of axes
    axes.scatter(data[x1], data[x2])
    axes.set_xlabel(xtitle, color=text_colour)  # Notice the use of set_ to begin methods
    axes.set_ylabel(ytitle, color=text_colour)

    # y=x line
    y_equals_x(data=data, x=x1, y=x2, colour="g--", axes=axes)

    # Label Points
    texts = []
    for i in np.arange(0, data.shape[0]):
        texts.append(
            plt.text(data[x1].iloc[i] - 0.02, data[x2].iloc[i] + 0.02, data[y].iloc[i], color=text_colour,
                     fontsize=label_size))
    adjust_text(texts)

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

def create_expected_player_graph(data, x1, x2, y, xtitle, ytitle, plottitle, gameweekrange):
    # Create Figure (empty canvas)
    fig, axes = plt.subplots(constrained_layout=True,dpi=100,figsize=[10,10])

    # Move set of axes to figure
    # axes = fig.add_axes([0, 0, 0.8, 0.8])  # left, bottom, width, height (range 0 to 1)

    # Hide grid lines
    axes.grid(False)

    # axis limits
    #plt.ylim(0, max(data[x1].max()+1,data[x2].max()+1))
    #plt.xlim(0, max(data[x1].max()+1,data[x2].max()+1))

    # colours
    plt.rcParams['figure.facecolor'] = back_colour
    axes.set_facecolor(back_colour)
    fig.patch.set_facecolor(back_colour)
    plt.rcParams["font.family"] = label_font
    axes.spines['left'].set_color(text_colour)
    axes.spines['bottom'].set_color(text_colour)
    axes.spines['top'].set_visible(False)
    axes.tick_params(axis='x', colors=text_colour)
    axes.tick_params(axis='y', colors=text_colour)

    if gameweekrange == "ALL":
        axes.set_title(f"{plottitle}\n 21/22 Season so far", color="w", loc="left", size=title_size, font=title_font)
    elif gameweekrange[0] == gameweekrange[1]:
        axes.set_title(f"{plottitle}\nGameweek {gameweekrange[0]}", color="w", loc="left", size=title_size,
                       font=title_font)
    else:
        axes.set_title(f"{plottitle}\nbetween gameweek {gameweekrange[0]} and {gameweekrange[1]}", color="w",
                       loc="left", size=title_size,
                       font=title_font)

    # Plot on that set of axes
    axes.scatter(data[x1], data[x2])
    axes.set_xlabel(xtitle, color=text_colour)  # Notice the use of set_ to begin methods
    axes.set_ylabel(ytitle, color=text_colour)

    # y=x line
    #y_equals_x(data=data, x=x1, y=x2, colour="g--", axes=axes)

    #Make any top performens transparent
    season=data["Season"].mode().iloc[0]

    # Label Points
    texts = []
    for i in np.arange(0, data.shape[0]):
        if (data["Season"].iloc[i]==season)==False:
            texts.append(
                plt.text(data[x1].iloc[i] - 0.02, data[x2].iloc[i] + 0.02, data[y].iloc[i], color=text_colour,
                         fontsize=label_size,fontstyle="italic",alpha=0.6))
        else:
            texts.append(
                plt.text(data[x1].iloc[i] - 0.02, data[x2].iloc[i] + 0.02, data[y].iloc[i], color=text_colour,
                         fontsize=label_size))
    adjust_text(texts)

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

def hbarplot(data, x1, x2, y, ytitle, xtitle, plottitle, gameweekrange):
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

def hbarplot_players(data, x1, x2, y, x1title,x2title,ytitle, plottitle, gameweekrange):
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
    axes.set(ylabel=ytitle)
    sns.despine(left=True, bottom=True)

def stacked_hbarplot_players(data,y, xtitle, plottitle, gameweekrange):
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

    #axes.set(ylabel=ytitle, xlabel=xtitle)
    sns.despine(left=True, bottom=True)

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