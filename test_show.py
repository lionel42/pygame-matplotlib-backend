import sys
import os
from numpy.ma.core import size
import pygame

import matplotlib
matplotlib.use('module://pygame_matplotlib.backend_pygame')
#matplotlib.use('Qt4Agg')

import matplotlib.pyplot as plt
import matplotlib.figure as fg

import matplotlib.image as mpimg

from examples import plot_error_bars_ex, plot_violin

fig, axes = plt.subplots(3,2,figsize=(16, 12))
print(type(fig))

axes[0, 0].plot([1,2], [1,2], color='green', label='test')
axes[0, 0].plot([1,2], [1,1], color='orange', lw=5, label='test other larger')
# axes[0, 0].legend()
axes[0, 1].text(0.5, 0.5, '2', size=50)
axes[1, 0].set_xlabel('swag')
axes[1, 0].fill_between([0, 1, 2], [1, 2, 3], [3, 4, 5])
axes[1, 0].scatter([0, 1, 2], [2, 3, 4], s=50)
axes[1, 1].imshow(mpimg.imread('images' + os.sep + 'long_dog.jpg'))
plot_error_bars_ex(axes[2, 1])
plot_violin(axes[2, 0])


plt.show()