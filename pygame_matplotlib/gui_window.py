"""Contain a window with a plot for pygame_gui."""
from typing import Union

import pygame
import pygame_gui
from pygame_gui.core.interfaces.manager_interface import IUIManagerInterface
from pygame_gui.core.ui_element import ObjectID

from .backend_pygame import FigureSurface
import matplotlib

matplotlib.use("module://pygame_matplotlib.backend_pygame")


class UIPlotWindow(pygame_gui.elements.ui_window.UIWindow):
    def __init__(
        self,
        rect: pygame.Rect,
        manager: IUIManagerInterface,
        figuresurface: FigureSurface,
        window_display_title: str = "",
        element_id: Union[str, None] = None,
        object_id: Union[ObjectID, str, None] = None,
        resizable: bool = False,
        visible: int = 1,
    ):
        self.figuresurf = figuresurface
        super().__init__(
            rect,
            manager,
            window_display_title=window_display_title,
            element_id=element_id,
            object_id=object_id,
            resizable=resizable,
            visible=visible,
        )

    def set_dimensions(self, *args, **kwargs):
        super().set_dimensions(*args, **kwargs)
        print("setting dimensions")
        # Update the size of the figure with the new bounding rectangle
        self.figuresurf.set_bounding_rect(self.get_container().get_rect())
        self.update_window_image()

    def update_window_image(self):
        # Update the image of the container
        self.get_container().set_image(self.figuresurf)
