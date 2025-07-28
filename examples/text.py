"""Taken from the matplotlib text example."""

import matplotlib.pyplot as plt
import logging

# Set up logging
logging.basicConfig()
logger = logging.getLogger("pygame_matplotlib")
logger.setLevel(logging.DEBUG)

import matplotlib

# matplotlib.use("pygame")

fig = plt.figure()
ax = fig.add_subplot()
fig.subplots_adjust(top=0.85)

# Set titles for the figure and the subplot respectively
fig.suptitle("bold figure suptitle", fontsize=14, fontweight="bold")
ax.set_title("axes title")

ax.set_xlabel("xlabel")
ax.set_ylabel("ylabel")

# Set both x- and y-axis limits to [0, 10] instead of default [0, 1]
ax.axis([0, 10, 0, 10])

ax.text(
    3,
    8,
    "boxed italics text in data coords",
    style="italic",
    bbox={"facecolor": "red", "alpha": 0.5, "pad": 10},
)

ax.text(2, 6, r"an equation: $E=mc^2$", fontsize=15)

ax.text(3, 2, "Unicode: Institut für Festkörperphysik")


ax.text(3, 5, "aaa", rotation=90)
ax.text(3, 5, "bbb", rotation=135)

ax.text(
    0.95,
    0.01,
    "colored text in axes coords",
    verticalalignment="bottom",
    horizontalalignment="right",
    transform=ax.transAxes,
    color="green",
    fontsize=15,
)

ax.plot([2], [1], "o")
ax.annotate(
    "annotate",
    xy=(2, 1),
    xytext=(3, 4),
    arrowprops=dict(facecolor="black", shrink=0.05),
)

plt.show()
