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
        '#1f77b4': {'marker': None, 'dash': [5,2]},
        '#ff7f0e': {'marker': None, 'dash': [3,4]},
        '#2ca02c': {'marker': None, 'dash': [1,1]},
        'k': {'marker': None, 'dash': (None,None)},
        "#d62728": {'marker': None, 'dash': (None,None)},
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


def save_figs(folder):
    happiness_diff = load_data_frame("{}/data/{}".format(folder, "_happy_increase.csv"))
    unhappiness_diff = load_data_frame("{}/data/{}".format(folder, "_unhappy_increase.csv"))

    happiness_diff['dictator'] = 0
    unhappiness_diff['dictator'] = 0

    happiness_total_all = load_data_frame("{}/data/{}".format(folder, "_happy_total_all.csv"))
    unhappiness_total_all = load_data_frame("{}/data/{}".format(folder, "_unhappy_total_all.csv"))

    column = happiness_total_all.columns[0]
    index = happiness_total_all.index[0]
    dictator_y_happy = happiness_total_all[column][index] - happiness_diff[column][index]
    dictator_y_unhappy = unhappiness_total_all[column][index] - unhappiness_diff[column][index]


    figure, axes = new_fig(title="{} Figure 2".format(folder))

    x_lim=[0,150]

    axes[0].set_title("satisfaction")
    axes[0].set_xlim(x_lim)
    axes[0].set_xlabel("number of stored configurations")
    axes[0].set_ylabel("number of people")
    axes[0].axhline(y=dictator_y_happy,linewidth=1, color='k')

    happiness_total_all.plot(ax=axes[0])
    y_labels_happy_total =axes[0].get_yticks().tolist()

    axes[1].set_title("dissatisfaction")
    axes[1].set_xlabel("number of stored configurations")
    axes[1].set_ylabel("number of people")
    axes[1].set_xlim(x_lim)
    axes[1].axhline(y=dictator_y_unhappy,linewidth=1, color='k')

    unhappiness_total_all.plot(ax=axes[1])
    y_labels_unhappy_total =axes[1].get_yticks().tolist()

    setFigLinesBW(figure)

    #plt.savefig("{}/fig/vis_happy_unhappy_number.pdf".format(folder),format="pdf")
    plt.close()

    figure, axes = new_fig(title="{} Figure 1".format(folder))

    x_lim=[0,150]

    left_y_label = "change in number of people"
    rigt_y_label = "number of people"
    x_label = "number of stored configurations"

    axes[0].set_title("satisfaction")
    axes[0].set_xlim(x_lim)
    axes[0].set_xlabel(x_label)
    axes[0].set_ylabel(left_y_label)
    #axes[0].axhline(y=0, linewidth=1, color='k')
    twin0 = axes[0].twinx()
    twin0.set_ylabel(rigt_y_label)

    happiness_diff.plot(ax=axes[0])

    axes[1].set_title("dissatisfaction")
    axes[1].set_xlabel(x_label)
    axes[1].set_ylabel(left_y_label)
    axes[1].set_xlim(x_lim)
    #axes[1].axhline(y=0, linewidth=1, color='k')
    twin1 = axes[1].twinx()
    twin1.set_ylabel(rigt_y_label)


    unhappiness_diff.plot(ax=axes[1])

    y_labels_happy = list(map(lambda x: process_label(x, show_plus=True), axes[0].get_yticks().tolist()))
    y_labels_unhappy = list(map(lambda x: process_label(x, show_plus=True), axes[1].get_yticks().tolist()))

    y_labels_secondary_happy = list(map(lambda x: process_label(x + dictator_y_happy), axes[0].get_yticks().tolist()))
    y_labels_secondary_unhappy = list(map(lambda x: process_label(x + dictator_y_unhappy), axes[1].get_yticks().tolist()))
    
    align_labels(axes[0], twin0)
    align_labels(axes[1], twin1)

    axes[0].set_yticklabels(y_labels_happy)
    twin0.set_yticklabels(y_labels_secondary_happy)

    axes[1].set_yticklabels(y_labels_unhappy)
    twin1.set_yticklabels(y_labels_secondary_unhappy)


    setFigLinesBW(figure)

    #plt.show()

    plt.savefig("{}/fig/vis_happy_unhappy_combined.pdf".format(folder),format="pdf")
    plt.close()

def process_label(label, show_plus=False, round_digits = 2):
    n_label = round(label, round_digits)
    if label > 0 and show_plus:
        n_label = "+{}".format(n_label)
    else:
        n_label = "{}".format(n_label)
    return n_label

def align_labels(origin, to_align):
    y_low, y_high =  origin.get_ylim()
    to_align.set_ylim(y_low, y_high)
    to_align.set_yticklabels(origin.get_yticks().tolist())


def load_data_frame(path):
    frame = pd.read_csv(path, index_col=0).T
    frame.index = frame.index.astype(int)
    return frame

def new_fig(subplot_row=1, subplot_column=2,aspect_ratio=1.3 ,dpi=300, title="Untitled"):
    figure, axes = plt.subplots(subplot_row, subplot_column, sharey=False)
    figure.canvas.set_window_title(title)
    figure.dpi = dpi
    figure.set_figwidth(4 * subplot_column * aspect_ratio)
    figure.set_figheight(4 * subplot_row)
    plt.subplots_adjust(wspace=0.45)

    return figure, axes


def main(dir = "./out"):
    for subdir in os.listdir(dir):
        path = "{}/{}".format(dir,subdir)
        if os.path.isdir(path):
            try: 
                save_figs(path)
                print("Generated Figures for: {}".format(subdir))
            except OSError as e:
                print("Files Not Found in: {}".format(subdir))

if __name__ == "__main__":
    main()