import sys
import os
from numpy.ma.core import size
import pygame

import matplotlib
matplotlib.use('pygame')
#matplotlib.use('Qt4Agg')

import matplotlib.pyplot as plt
import matplotlib.figure as fg

import matplotlib.pyplot as plt



def test_save_jpg():
    plt.figure()


    plt.plot([1,2], [1,2], color='green')
    plt.text(1.5, 1.5, '2', size=50)
    plt.xlabel('swag')

    plt.savefig('images' + os.sep + 'test.jpg')


def test_save_bmp():
    plt.figure()
    plt.plot([1,2], [1,2], color='green')
    plt.text(1.5, 1.5, '2', size=50)
    plt.xlabel('swag')
    plt.savefig('images' + os.sep + 'test.bmp')
