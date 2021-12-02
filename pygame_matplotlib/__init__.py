import pygame


def pygame_color_to_plt(color: pygame.Color):
    """Convert a pygame Color to a matplot lib value."""
    # Interval from 0 to 1 in matplotlib
    return tuple(
        value / 255.0 for value in [color.r, color.g, color.b, color.a]
    )
