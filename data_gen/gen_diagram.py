import matplotlib.pyplot as plt
import pandas as pd
import os

def setAxLinesBW(ax):
    """
    Take each Line2D in the axes, ax, and convert the line style to be 
    suitable for black and white viewing.
    """
    MARKERSIZE = 3

    COLORMAP = {
        '#ff7f0e': {'marker': None, 'dash': [3,4]},
        '#1f77b4': {'marker': None, 'dash': [1,1]},
        '#2ca02c': {'marker': None, 'dash': (None,None)}
        }


    lines_to_adjust = ax.get_lines()
    try:
        lines_to_adjust += ax.get_legend().get_lines()
    except AttributeError:
        pass

    for line in lines_to_adjust:
        origColor = line.get_color()
        line.set_color('black')
        line.set_dashes(COLORMAP[origColor]['dash'])
        line.set_marker(COLORMAP[origColor]['marker'])
        line.set_markersize(MARKERSIZE)

def setFigLinesBW(fig):
    """
    Take each axes in the figure, and for each line in the axes, make the
    line viewable in black and white.
    """
    for ax in fig.get_axes():
        setAxLinesBW(ax)

def load_data_frame(path):
    frame = pd.read_csv(path, index_col=0).T
    frame.index = frame.index.astype(int)
    return frame

def new_fig(subplot_row=1, subplot_column=2, dpi=300, title="Untitled"):
    figure, axes = plt.subplots(subplot_row, subplot_column, sharey=True)
    #figure.tight_layout(pad=1.5)
    for axis in axes:
        axis.tick_params(
            axis="y",       # both major and minor ticks are affected
            left=True,
            labelleft=True,
            labelright=True)
    figure.canvas.set_window_title(title)
    figure.dpi = dpi
    figure.set_figwidth(4 * subplot_column)
    figure.set_figheight(4 * subplot_row)

    return axes


happy_dictator = load_data_frame("./{}".format("happy_dictator.csv"))
unhappy_dictator = load_data_frame("./{}".format("unhappy_dictator.csv"))

axes = new_fig()

axes[0].set_title("satisfaction")
#axes[0].set_xlim(x_lim)
axes[0].set_xlabel("tc")
axes[0].set_ylabel("number of people")

happy_dictator.plot(ax=axes[0])

setAxLinesBW(axes[0])

axes[1].set_title("dissatisfaction")
axes[1].set_xlabel("tc")
axes[1].set_ylabel("number of people")
#axes[1].set_xlim(x_lim)
unhappy_dictator.plot(ax=axes[1])

setAxLinesBW(axes[1])

plt.savefig("./dictator.pdf",format="pdf")


happy_change = load_data_frame("./{}".format("happy_change.csv"))
unhappy_change = load_data_frame("./{}".format("unhappy_change.csv"))

axes = new_fig()

axes[0].set_title("satisfaction change")
#axes[0].set_xlim(x_lim)
axes[0].set_xlabel("tc")
axes[0].set_ylabel("number of people")

happy_change.plot(ax=axes[0])

setAxLinesBW(axes[0])

axes[1].set_title("dissatisfaction change")
axes[1].set_xlabel("tc")
axes[1].set_ylabel("number of people")
#axes[1].set_xlim(x_lim)
unhappy_change.plot(ax=axes[1])

setAxLinesBW(axes[1])

plt.savefig("./change.pdf",format="pdf")




plt.show()
plt.close()