import sys
import os
from numpy.ma.core import size
import pygame

import matplotlib

matplotlib.use("module://pygame_matplotlib.backend_pygame")
# matplotlib.use('Qt4Agg')

import matplotlib.pyplot as plt
import matplotlib.figure as fg

plt.figure(figsize=(16, 9))
plt.plot([1, 2], [1, 2], color="green", label="HAHA")
plt.text(1.5, 1.5, "2", size=50)
plt.xlabel("swag")
plt.legend()


plt.show()
