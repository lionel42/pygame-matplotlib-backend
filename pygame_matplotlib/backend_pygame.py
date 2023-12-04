"""Pygame Matplotlib Backend.

A functional backend for using matplotlib in pygame display.
You can select it as a backend using
with ::

    import matplotlib
    matplotlib.use("'module://pygame_matplotlib.backend_pygame'")
"""
from __future__ import annotations

from typing import List
import matplotlib
from matplotlib.artist import Artist
from matplotlib.pyplot import figure
from matplotlib.axes import Axes
from matplotlib.transforms import IdentityTransform
import numpy as np
from matplotlib.transforms import Affine2D
import pygame
import pygame.image
from pygame import gfxdraw
from matplotlib._pylab_helpers import Gcf
from matplotlib.backend_bases import (
    FigureCanvasBase,
    FigureManagerBase,
    GraphicsContextBase,
    RendererBase,
)
from matplotlib.figure import Figure
from matplotlib.path import Path
from matplotlib.transforms import Bbox

import logging

logger = logging.getLogger(__name__)
console = logging.StreamHandler()
logger.addHandler(console)

logger.setLevel(logging.WARNING)

logger.warning(
    f"{__name__} is still in developpement. Please see our github page."
)


class FigureSurface(pygame.Surface, Figure):
    """Hybrid object mixing pygame.Surface and matplotlib.Figure.

    The functionality of both objects is kept with some special features
    that help handling the figures in pygame.
    """

    canvas: FigureCanvasPygame
    animated_artists: List[Artist]

    def __init__(self, *args, **kwargs):
        """Create a FigureSurface object.

        Signature is the same as matplotlib Figure object.
        """
        Figure.__init__(self, *args, **kwargs)
        pygame.Surface.__init__(self, self.bbox.size)
        # self.fill("white")

    def set_bounding_rect(self, rect: pygame.Rect):
        """Set a bounding rectangle around the figure."""
        # First convert inches to pixels for matplotlib
        DPI = self.get_dpi()
        self.set_size_inches(rect.width / float(DPI), rect.height / float(DPI))
        # Initialize a new surface for the plot
        pygame.Surface.__init__(self, (rect.width, rect.height))
        # Redraw the figure
        self.canvas.draw()

    def draw(self, renderer):
        return super().draw(renderer)

    def set_alpha(self):
        pass

    def set_at(self):
        pass

    def set_clip(self):
        pass

    def set_colorkey(self):
        pass

    def set_masks(self):
        pass

    def set_palette(self):
        pass

    def set_palette_at(self):
        pass

    def set_shifts(self):
        pass

    def get_interactive_artists(self, renderer):
        """Get the interactive artists.

        Custom method used for the blitting.
        Modification of _get_draw_artists
        Also runs apply_aspect.
        """
        artists = self.get_children()

        for sfig in self.subfigs:
            artists.remove(sfig)
            childa = sfig.get_children()
            for child in childa:
                if child in artists:
                    artists.remove(child)

        artists.remove(self.patch)
        artists = sorted(
            (artist for artist in artists if artist.get_animated()),
            key=lambda artist: artist.get_zorder(),
        )

        for ax in self._localaxes.as_list():
            locator = ax.get_axes_locator()

            if locator:
                pos = locator(ax, renderer)
                ax.apply_aspect(pos)
            else:
                ax.apply_aspect()

            for child in ax.get_children():
                if child.get_animated():
                    artists.append(child)
                if hasattr(child, "apply_aspect"):
                    locator = child.get_axes_locator()
                    if locator:
                        pos = locator(child, renderer)
                        child.apply_aspect(pos)
                    else:
                        child.apply_aspect()

        return artists


class RendererPygame(RendererBase):
    """The renderer handles drawing/rendering operations.

    The draw methods convert maptplotlib into pygame.draw .
    """

    surface: pygame.Surface

    def __init__(self, dpi):
        super().__init__()
        self.dpi = dpi

    def rect_from_bbox(self, bbox: Bbox) -> pygame.Rect:
        """Convert a matplotlib bbox to the equivalent pygame Rect."""
        raise NotImplementedError()

    def draw_path(self, gc, path, transform, rgbFace=None):
        """Draw a path using pygame functions."""
        if rgbFace is not None:
            color = tuple(
                [int(val * 255) for i, val in enumerate(rgbFace) if i < 3]
            )
        else:
            color = tuple(
                [int(val * 255) for i, val in enumerate(gc.get_rgb()) if i < 3]
            )

        linewidth = int(gc.get_linewidth())

        transfrom_to_pygame_axis = Affine2D()
        transfrom_to_pygame_axis.set_matrix(
            [[1, 0, 0], [0, -1, self.surface.get_height()], [0, 0, 1]]
        )
        if not isinstance(transform, IdentityTransform):
            transform += transfrom_to_pygame_axis

        draw_func = (
            # Select whether antialiased will be used in pygame
            # Antialiased cannot hanlde linewidth > 1
            pygame.draw.aaline
            if gc.get_antialiased() and linewidth <= 1
            else pygame.draw.line
        )

        previous_point = (0, 0)
        poly_points = []

        for point, code in path.iter_segments(transform):
            logger.debug(point, code)
            if code == Path.LINETO:
                draw_func(
                    self.surface, color, previous_point, point, linewidth
                )
                previous_point = point
                poly_points.append(point)
            elif code == Path.CURVE3 or code == Path.CURVE4:
                end_point = point[2:]
                points_curve = np.concatenate((previous_point, point)).reshape(
                    (-1, 2)
                )
                gfxdraw.bezier(
                    self.surface, points_curve, len(points_curve), color
                )
                previous_point = end_point
                poly_points.append(end_point)
            elif code == Path.CLOSEPOLY:
                if len(poly_points) > 2:
                    gfxdraw.filled_polygon(self.surface, poly_points, color)
            elif code == Path.MOVETO:
                poly_points.append(point)
                previous_point = point
            else:  # STOP
                previous_point = point

    # draw_markers is optional, and we get more correct relative
    # timings by leaving it out.  backend implementers concerned with
    # performance will probably want to implement it
    #     def draw_markers(self, gc, marker_path, marker_trans, path, trans,
    #                      rgbFace=None):
    #         pass

    # draw_path_collection is optional, and we get more correct
    # relative timings by leaving it out. backend implementers concerned with
    # performance will probably want to implement it
    #     def draw_path_collection(self, gc, master_transform, paths,
    #                              all_transforms, offsets, offsetTrans,
    #                              facecolors, edgecolors, linewidths, linestyles,
    #                              antialiaseds):
    #         pass

    # draw_quad_mesh is optional, and we get more correct
    # relative timings by leaving it out.  backend implementers concerned with
    # performance will probably want to implement it
    #     def draw_quad_mesh(self, gc, master_transform, meshWidth, meshHeight,
    #                        coordinates, offsets, offsetTrans, facecolors,
    #                        antialiased, edgecolors):
    #         pass

    def draw_image(self, gc, x, y, im):
        img_surf = pygame.image.frombuffer(
            # Need to flip the image as pygame starts top left
            np.ascontiguousarray(np.flip(im, axis=0)),
            (im.shape[1], im.shape[0]),
            "RGBA",
        )
        self.surface.blit(
            img_surf,
            # Image starts top left
            (x, self.surface.get_height() - y - im.shape[0]),
        )

    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        # make sure font module is initialized
        if not pygame.font.get_init():
            pygame.font.init()
        # prop is the font properties
        font_size = prop.get_size_in_points() * 2
        myfont = pygame.font.Font(prop.get_file(), int(font_size))
        # apply it to text on a label
        font_surface = myfont.render(
            s, gc.get_antialiased(), [val * 255 for val in gc.get_rgb()]
        )
        # Get the expected size of the font
        width, height = myfont.size(s)
        # Tuple for the position of the font
        font_surf_position = (x, self.surface.get_height() - y)
        if mtext is not None:
            # Use the alignement from mtext or default
            h_alignment = mtext.get_horizontalalignment()
            v_alignment = mtext.get_verticalalignment()
        else:
            h_alignment = "center"
            v_alignment = "center"
        # Use the alignement to know where the font should go
        if h_alignment == "left":
            h_offset = 0
        elif h_alignment == "center":
            h_offset = -width / 2
        elif h_alignment == "right":
            h_offset = -width
        else:
            h_offset = 0

        if v_alignment == "top":
            v_offset = 0
        elif v_alignment == "center" or v_alignment == "center_baseline":
            v_offset = -height / 2
        elif v_alignment == "bottom" or v_alignment == "baseline":
            v_offset = -height
        else:
            v_offset = 0
        # pygame.draw.circle(self.surface, (255, 0, 0), (x, self.surface.get_height() - y), 3)
        # pygame.draw.lines(self.surface, (0, 255, 0), True, ((x, self.surface.get_height() - y), (x + width, self.surface.get_height() - y), (x + width, self.surface.get_height() - y + height)))
        # Tuple for the position of the font
        font_surf_position = (
            x + h_offset,
            self.surface.get_height() - y + v_offset,
        )
        self.surface.blit(font_surface, font_surf_position)

    def flipy(self):
        # docstring inherited
        return False

    def get_canvas_width_height(self):
        # docstring inherited
        return 100, 100

    def get_text_width_height_descent(self, s, prop, ismath):
        return 1, 1, 1

    def new_gc(self):
        # docstring inherited
        return GraphicsContextPygame()

    def points_to_pixels(self, points):
        # points are pixels in pygame
        return points
        # elif backend assumes a value for pixels_per_inch
        # return points/72.0 * self.dpi.get() * pixels_per_inch/72.0
        # else
        # return points/72.0 * self.dpi.get()

    def clear(self):
        self.surface.fill("white")

    def copy_from_bbox(self, bbox):
        copy = self.surface.copy()
        copy.bbox = bbox
        return copy


class GraphicsContextPygame(GraphicsContextBase):
    """
    The graphics context provides the color, line styles, etc...  See the cairo
    and postscript backends for examples of mapping the graphics context
    attributes (cap styles, join styles, line widths, colors) to a particular
    backend.  In cairo this is done by wrapping a cairo.Context object and
    forwarding the appropriate calls to it using a dictionary mapping styles
    to gdk constants.  In Postscript, all the work is done by the renderer,
    mapping line styles to postscript calls.

    If it's more appropriate to do the mapping at the renderer level (as in
    the postscript backend), you don't need to override any of the GC methods.
    If it's more appropriate to wrap an instance (as in the cairo backend) and
    do the mapping here, you'll need to override several of the setter
    methods.

    The base GraphicsContext stores colors as a RGB tuple on the unit
    interval, e.g., (0.5, 0.0, 1.0). You may need to map this to colors
    appropriate for your backend.
    """


########################################################################
#
# The following functions and classes are for pyplot and implement
# window/figure managers, etc...
#
########################################################################


def draw_if_interactive():
    """
    For image backends - is not required.
    For GUI backends - this should be overridden if drawing should be done in
    interactive python mode.
    """


def show(*, block=None):
    """
    For image backends - is not required.
    For GUI backends - show() is usually the last line of a pyplot script and
    tells the backend that it is time to draw.  In interactive mode, this
    should do nothing.
    """
    for manager in Gcf.get_all_fig_managers():
        manager.show(block)


def new_figure_manager(num, *args, FigureClass=FigureSurface, **kwargs):
    """Create a new figure manager instance."""
    # If a main-level app must be created, this (and
    # new_figure_manager_given_figure) is the usual place to do it -- see
    # backend_wx, backend_wxagg and backend_tkagg for examples.  Not all GUIs
    # require explicit instantiation of a main-level app (e.g., backend_gtk3)
    # for pylab.

    # Pygame surfaces require surface objects
    thisFig = FigureSurface(*args, **kwargs)
    return new_figure_manager_given_figure(num, thisFig)


def new_figure_manager_given_figure(num, figure):
    """Create a new figure manager instance for the given figure."""
    canvas = FigureCanvasPygame(figure)
    manager = FigureManagerPygame(canvas, num)
    return manager


class FigureCanvasPygame(FigureCanvasBase):
    """
    The canvas the figure renders into.  Calls the draw and print fig
    methods, creates the renderers, etc.

    Note: GUI templates will want to connect events for button presses,
    mouse movements and key presses to functions that call the base
    class methods button_press_event, button_release_event,
    motion_notify_event, key_press_event, and key_release_event.  See the
    implementations of the interactive backends for examples.

    Attributes
    ----------
    figure : `matplotlib.figure.Figure`
        A high-level Figure instance
    """

    blitting: bool = False

    # File types allowed for saving
    filetypes = {
        "jpeg": "Joint Photographic Experts Group",
        "jpg": "Joint Photographic Experts Group",
        "png": "Portable Network Graphics",
        "bmp": "Bitmap Image File",
        "tga": "Truevision Graphics Adapter",
    }
    figure: FigureSurface
    renderer: RendererPygame
    main_display: pygame.Surface

    def __init__(self, figure=None):
        super().__init__(figure)

        # You should provide a print_xxx function for every file format
        # you can write.
        for file_extension in self.filetypes.keys():
            setattr(self, "print_{}".format(file_extension), self._print_any)

    def copy_from_bbox(self, bbox):
        renderer = self.get_renderer()
        return renderer.copy_from_bbox(bbox)

    def restore_region(self, region, bbox=None, xy=None):
        rect = (
            pygame.Rect(
                *(0, 0 if xy is None else xy),
                *self.get_renderer().surface.get_size(),
            )
            if bbox is None
            else self.rect_from_bbox(bbox)
        )
        self.figure.blit(region, rect)

    def draw(self):
        """
        Draw the figure using the renderer.

        It is important that this method actually walk the artist tree
        even if not output is produced because this will trigger
        deferred work (like computing limits auto-limits and tick
        values) that users may want access to before saving to disk.
        """
        self.renderer = self.get_renderer(cleared=True)
        self.renderer.surface = self.figure
        if self.blitting:
            # Draw only interactive artists
            artists = self.figure.get_interactive_artists(self.renderer)
            for a in artists:
                a.draw(self.renderer)
        else:
            # Full redraw of the figure
            self.figure.draw(self.renderer)

    def blit(self, bbox=None):
        self.renderer = self.get_renderer(cleared=False)
        self.renderer.surface = self.figure
        self.blitting = True

    def get_renderer(self, cleared=False) -> RendererPygame:
        fig = self.figure
        reuse_renderer = (
            hasattr(self, "renderer")
            and getattr(self, "_last_fig", None) == fig
        )
        if not reuse_renderer:
            self.renderer = RendererPygame(self.figure.dpi)
            self._last_fig = fig
        elif cleared:
            self.renderer.clear()
        return self.renderer

    def _print_any(self, filename, *args, **kwargs):
        """Call the pygame image saving method for the correct extenstion."""
        self.draw()
        pygame.image.save(self.figure, filename)

    def get_default_filetype(self):
        return "jpg"

    def flush_events(self):
        self.main_display.blit(self.figure, (0, 0))
        pygame.display.update()
        self.pygame_quit_event_check()

    def pygame_quit_event_check(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()

    def start_event_loop(self, interval: float):
        FPS = 60
        FramePerSec = pygame.time.Clock()
        time_elapsed = 0
        while time_elapsed < interval:
            events = pygame.event.get()
            time_elapsed += FramePerSec.tick(FPS) / 1000.0  # Convert ms
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()


class FigureManagerPygame(FigureManagerBase):
    """
    Helper class for pyplot mode, wraps everything up into a neat bundle.

    For non-interactive backends, the base class is sufficient.
    """

    canvas: FigureCanvasPygame

    def get_main_display(self):
        if hasattr(self.canvas, "main_display"):
            if (
                self.canvas.figure.get_size()
                == self.canvas.main_display.get_size()
            ):
                # If the main display exist and its size has not changed
                return self.canvas.main_display
        main_display = pygame.display.set_mode(
            self.canvas.figure.get_size(),  # Size matches figure size
        )
        main_display.fill("white")
        self.canvas.main_display = main_display
        return main_display

    def show(self, block=True):
        # do something to display the GUI
        pygame.init()
        main_display = self.get_main_display()

        FPS = 60
        FramePerSec = pygame.time.Clock()

        if not self.canvas.blitting:
            # Draw if we are not blitting
            self.canvas.draw()
        main_display.blit(self.canvas.figure, (0, 0))
        pygame.display.update()

        show_fig = True if block is None else False
        while show_fig:
            events = pygame.event.get()
            pygame.display.update()
            FramePerSec.tick(FPS)

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    show_fig = False


########################################################################
#
# Now just provide the standard names that backend.__init__ is expecting
#
########################################################################

FigureCanvas = FigureCanvasPygame
FigureManager = FigureManagerPygame
