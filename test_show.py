import sys
import os
from numpy.ma.core import size
import pygame

import matplotlib
matplotlib.use('module://pygame_matplotlib.backend_pygame')

import matplotlib.pyplot as plt
import matplotlib.figure as fg

fig, ax = plt.subplots(figsize=(16, 9))
print(type(fig))
ax.plot([1,2], [1,2], color='green')
ax.text(1.5, 1.5, '2', size=50)
ax.set_xlabel('swag')

fig.show()