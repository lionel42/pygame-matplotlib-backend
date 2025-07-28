import os

import matplotlib

matplotlib.use("pygame")

import matplotlib.pyplot as plt


def test_save_jpg():
    plt.figure()
    plt.plot([1, 2], [1, 2], color="green")
    plt.text(1.5, 1.5, "2", size=50)
    plt.xlabel("swag")
    plt.savefig("images" + os.sep + "test.jpg")


def test_save_bmp():
    plt.figure()
    plt.plot([1, 2], [1, 2], color="green")
    plt.text(1.5, 1.5, "2", size=50)
    plt.xlabel("swag")
    plt.savefig("images" + os.sep + "test.bmp")
