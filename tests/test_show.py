import os
import numpy as np

import matplotlib

# matplotlib.use('pygame')
matplotlib.use("pygame")

import matplotlib.pyplot as plt

import matplotlib.image as mpimg


def plot_error_bars_ex(ax):
    # example data
    x = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
    y = np.exp(-x)
    xerr = 0.1
    yerr = 0.2

    # lower & upper limits of the error
    lolims = np.array([0, 0, 1, 0, 1, 0, 0, 0, 1, 0], dtype=bool)
    uplims = np.array([0, 1, 0, 0, 0, 1, 0, 0, 0, 1], dtype=bool)
    ls = "dotted"

    # standard error bars
    ax.errorbar(x, y, xerr=xerr, yerr=yerr, linestyle=ls)

    # including upper limits
    ax.errorbar(x, y + 0.5, xerr=xerr, yerr=yerr, uplims=uplims, linestyle=ls)

    # including lower limits
    ax.errorbar(x, y + 1.0, xerr=xerr, yerr=yerr, lolims=lolims, linestyle=ls)

    # including upper and lower limits
    ax.errorbar(
        x,
        y + 1.5,
        xerr=xerr,
        yerr=yerr,
        lolims=lolims,
        uplims=uplims,
        marker="o",
        markersize=8,
        linestyle=ls,
    )

    # Plot a series with lower and upper limits in both x & y
    # constant x-error with varying y-error
    xerr = 0.2
    yerr = np.full_like(x, 0.2)
    yerr[[3, 6]] = 0.3

    # mock up some limits by modifying previous data
    xlolims = lolims
    xuplims = uplims
    lolims = np.zeros_like(x)
    uplims = np.zeros_like(x)
    lolims[[6]] = True  # only limited at this index
    uplims[[3]] = True  # only limited at this index

    # do the plotting
    ax.errorbar(
        x,
        y + 2.1,
        xerr=xerr,
        yerr=yerr,
        xlolims=xlolims,
        xuplims=xuplims,
        uplims=uplims,
        lolims=lolims,
        marker="o",
        markersize=8,
        linestyle="none",
    )

    # tidy up the figure
    ax.set_xlim((0, 5.5))
    ax.set_title("Errorbar upper and lower limits")


def plot_violin(ax):
    def adjacent_values(vals, q1, q3):
        upper_adjacent_value = q3 + (q3 - q1) * 1.5
        upper_adjacent_value = np.clip(upper_adjacent_value, q3, vals[-1])

        lower_adjacent_value = q1 - (q3 - q1) * 1.5
        lower_adjacent_value = np.clip(lower_adjacent_value, vals[0], q1)
        return lower_adjacent_value, upper_adjacent_value

    def set_axis_style(ax, labels):
        ax.xaxis.set_tick_params(direction="out")
        ax.xaxis.set_ticks_position("bottom")
        ax.set_xticks(np.arange(1, len(labels) + 1))
        ax.set_xticklabels(labels)
        ax.set_xlim(0.25, len(labels) + 0.75)
        ax.set_xlabel("Sample name")

    # create test data
    np.random.seed(19680801)
    data = [sorted(np.random.normal(0, std, 100)) for std in range(1, 5)]

    ax.set_title("Customized violin plot")
    parts = ax.violinplot(data, showmeans=False, showmedians=False, showextrema=False)

    for pc in parts["bodies"]:
        pc.set_facecolor("#D43F3A")
        pc.set_edgecolor("black")
        pc.set_alpha(1)

    quartile1, medians, quartile3 = np.percentile(data, [25, 50, 75], axis=1)
    whiskers = np.array(
        [
            adjacent_values(sorted_array, q1, q3)
            for sorted_array, q1, q3 in zip(data, quartile1, quartile3)
        ]
    )
    whiskers_min, whiskers_max = whiskers[:, 0], whiskers[:, 1]

    inds = np.arange(1, len(medians) + 1)
    ax.scatter(inds, medians, marker="o", color="white", s=30, zorder=3)
    ax.vlines(inds, quartile1, quartile3, color="k", linestyle="-", lw=5)
    ax.vlines(inds, whiskers_min, whiskers_max, color="k", linestyle="-", lw=1)

    # set style for the axes
    labels = ["A", "B", "C", "D"]
    set_axis_style(ax, labels)


def test_multiplot():
    fig, axes = plt.subplots(3, 2, figsize=(16, 12))

    axes[0, 0].plot([1, 2], [1, 2], color="green", label="test")
    axes[0, 0].plot([1, 2], [1, 1], color="orange", lw=5, label="test other larger")
    # axes[0, 0].legend()
    axes[0, 1].text(0.5, 0.5, "2", size=50)
    axes[1, 0].set_xlabel("swag")
    axes[1, 0].fill_between([0, 1, 2], [1, 2, 3], [3, 4, 5])
    axes[1, 0].scatter([0, 1, 2], [2, 3, 4], s=50)
    axes[1, 1].imshow(mpimg.imread("images" + os.sep + "long_dog.jpg"))
    plot_error_bars_ex(axes[2, 1])

    plot_violin(axes[2, 0])

    plt.show(block=False)
    plt.close(fig)
