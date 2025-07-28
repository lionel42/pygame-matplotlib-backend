import matplotlib

matplotlib.use("pygame")
import matplotlib.pyplot as plt

import pygame


def test_in_game_loop():
    fig, axes = plt.subplots(1, 1)
    axes.plot([1, 2], [1, 2], color="green", label="test")

    fig.canvas.draw()

    screen = pygame.display.set_mode((800, 600))
    screen.blit(fig, (100, 100))

    show = True
    i = 0
    while show:
        if i > 2:
            show = False
        pygame.display.update()
        i += 1
