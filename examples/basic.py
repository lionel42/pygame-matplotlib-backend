"""The most basic example of how to use the pygame-matplotlib backend."""

# Select pygame backend
import matplotlib
import logging
import matplotlib.pyplot as plt

logging.basicConfig()
logger = logging.getLogger("pygame_matplotlib")
logger.setLevel(logging.DEBUG)
matplotlib.use("pygame")


fig, ax = plt.subplots()  # Create a figure containing a single axes.
ax.plot([1, 2, 3, 4], [2, 4, 2, 9])  # Plot some data on the axes.
ax.set_ylabel("some y numbers")  # Add a y-label to the axes.
ax.set_xlabel("some x numbers")  # Add an x-label to the axes.
ax.set_xticklabels(
    # Long rotated labels
    ["label1", "label2", "label3", "label4"],
    rotation=45,
)
plt.show()
