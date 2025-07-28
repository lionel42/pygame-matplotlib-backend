"""Simple script to test from https://pygame-gui.readthedocs.io/en/latest/quick_start.html"""

import pygame
import pygame_gui

import matplotlib.pyplot as plt

from pygame_matplotlib.gui_window import UIPlotWindow


def test_gui_window():
    pygame.init()

    pygame.display.set_caption("Test")
    window_surface = pygame.display.set_mode((800, 600))

    background = pygame.Surface((800, 600))
    background.fill(pygame.Color("#000000"))

    manager = pygame_gui.UIManager((800, 600))

    fig, axes = plt.subplots(1, 1)
    axes.plot([1, 2], [1, 2], color="green", label="test")
    fig.canvas.draw()

    fig2, axes2 = plt.subplots(1, 1)
    axes2.plot([1, 2], [1, 2], color="blue", label="test")
    fig2.canvas.draw()

    plot_window = UIPlotWindow(
        rect=pygame.Rect((350, 275), (300, 200)),
        manager=manager,
        figuresurface=fig,
        resizable=True,
    )

    plot_window2 = UIPlotWindow(
        rect=pygame.Rect((350, 275), (200, 200)),
        manager=manager,
        figuresurface=fig2,
        resizable=False,
    )

    assert isinstance(plot_window, UIPlotWindow)
    assert isinstance(plot_window2, UIPlotWindow)

    clock = pygame.time.Clock()

    is_running = True
    i = 0

    while is_running:
        if i > 2:
            is_running = False
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            manager.process_events(event)

        manager.update(time_delta)

        # Blitts and draw
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        # print(plot_window2.get_container().get_size())

        pygame.display.update()
        i += 1
