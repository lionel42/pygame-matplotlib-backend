import sys
import os
from numpy.ma.core import size
import pygame

import matplotlib
matplotlib.use('module://pygame_matplotlib.backend_pygame')
# matplotlib.use('Qt4Agg')

import matplotlib.pyplot as plt
import matplotlib.figure as fg

import matplotlib.image as mpimg

fig, axes = plt.subplots(2,2,figsize=(16, 9))
print(type(fig))
axes[0, 0].plot([1,2], [1,2], color='green')
axes[0, 1].text(0.5, 0.5, '2', size=50)
axes[1, 0].set_xlabel('swag')
axes[1, 1].imshow(mpimg.imread('images' + os.sep + 'long_dog.jpg'))


plt.show()