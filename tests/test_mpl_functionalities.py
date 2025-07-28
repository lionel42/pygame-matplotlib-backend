import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("pygame")


def test_save_jpg():
    plt.figure()
    plt.plot([1, 2], [1, 2], color="green")
    plt.text(1.5, 1.5, "2", size=50)


def test_tight_layout():
    plt.figure()
    plt.plot([1, 2], [1, 2], color="green")
    plt.text(1.5, 1.5, "2", size=50)
    plt.tight_layout()


def test_ylabel():
    # Issue that the ylabel was not reotated, sadly I cannot  visually test this
    plt.figure()
    plt.plot([1, 2], [1, 2], color="green")
    plt.text(1.5, 1.5, "2", size=50)
    plt.ylabel("swag")
    plt.tight_layout()
