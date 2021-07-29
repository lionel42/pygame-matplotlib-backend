"""
A fully functional, do-nothing backend intended as a template for backend
writers.  It is fully functional in that you can select it as a backend e.g.
with ::

    import matplotlib
    matplotlib.use("template")

and your program will (should!) run without error, though no output is
produced.  This provides a starting point for backend writers; you can
selectively implement drawing methods (`~.RendererTemplate.draw_path`,
`~.RendererTemplate.draw_image`, etc.) and slowly see your figure come to life
instead having to have a full blown implementation before getting any results.

Copy this file to a directory outside of the Matplotlib source tree, somewhere
where Python can import it (by adding the directory to your ``sys.path`` or by
packaging it as a normal Python package); if the backend is importable as
``import my.backend`` you can then select it using ::

    import matplotlib
    matplotlib.use("module://my.backend")

If your backend implements support for saving figures (i.e. has a `print_xyz`
method), you can register it as the default handler for a given file type::

    from matplotlib.backend_bases import register_backend
    register_backend('xyz', 'my_backend', 'XYZ File Format')
    ...
    plt.savefig("figure.xyz")
"""
from matplotlib.transforms import Affine2D
import pygame
from matplotlib._pylab_helpers import Gcf
from matplotlib.backend_bases import (
     FigureCanvasBase, FigureManagerBase, GraphicsContextBase, RendererBase)
from matplotlib.figure import Figure
from matplotlib.path import Path
import math

class FigureSurface(pygame.Surface, Figure):
    def __init__(self, *args, **kwargs):
        print("initialized")
        Figure.__init__(self, *args, **kwargs)
        pygame.Surface.__init__(self, self.bbox.size)
        self.fill('white')

class RendererTemplate(RendererBase):
    """
    The renderer handles drawing/rendering operations.

    This is a minimal do-nothing class that can be used to get started when
    writing a new backend.  Refer to `backend_bases.RendererBase` for
    documentation of the methods.
    """

    def __init__(self, dpi):
        super().__init__()
        self.dpi = dpi


    def draw_path(self, gc, path, transform, rgbFace=None):

        if rgbFace is None:
            rgbFace = gc.get_rgb()
        color = tuple([int(val*255) for i, val in enumerate(rgbFace) if i < 3])

        linewidth = int(gc.get_linewidth())

        transfrom_to_pygame_axis = Affine2D()
        transfrom_to_pygame_axis.set_matrix([
            [1, 0, 0], [0, -1, self.surface.get_height()], [0, 0, 1]
        ])

        transform += transfrom_to_pygame_axis

        draw_func =  pygame.draw.aaline if gc.get_antialiased() else pygame.draw.line

        previous_point = (0, 0)
        for point, code in path.iter_segments(transform):
            # previous_point = point
            # print(point, code)
            if code == Path.LINETO:
                draw_func(
                    self.surface, color, previous_point, point, linewidth
                )
                previous_point = point
            elif code == Path.CURVE3:
                end_point = point[2:]
                control_point = point[:2]
                # Creates the bounding rectangle for the arc
                # rect = pygame.Rect(
                #     x:=min(previous_point[0], end_point[0]),
                #     y:=min(previous_point[1], end_point[1]),
                #     w:=max(previous_point[0], end_point[0]) - x,
                #     h:=max(previous_point[1], end_point[1]) - y,
                # )
                # start_angle = math.atan(abs(
                #     (x - control_point[0])
                #     / (y- control_point[1])
                # ))
                # stop_angle = math.atan(abs(
                #     (x + w - control_point[0])
                #     / (y + h - control_point[1])
                # ))
                # Find the vectors to get the angle of the arc
                #c_p = (control_point[0] - previous_point[0], control_point[1] - previous_point[1])
                #c_e = (control_point[0] - end_point[0], control_point[1] - end_point[1])
                #arc_angle = math.acos(
                #    ((c_p[0] * c_e[0]) + (c_p[1] * c_e[1]))
                #    / (math.hypot(*c_p) * math.hypot(*c_e))
                #)
                # The focals are at the intersection
                draw_func(
                    self.surface, color, previous_point, end_point, linewidth
                )
                previous_point = end_point
            else:
                previous_point = point
        pass

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
        pass

    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        # make sure font module is initialized
        if not pygame.font.get_init():
            pygame.font.init()
        # prop is the fondt properties
        font_size = prop.get_size() * self.dpi / 57
        myfont = pygame.font.Font(prop.get_file(), int(font_size))
        # apply it to text on a label
        font_surface = myfont.render(
            s, gc.get_antialiased(), [val*255 for val in gc.get_rgb()]
        )
        if mtext is not None:
            # Reads the position of the mtext, but could use relative position to 0 instead
            x, y, _, _ = mtext.get_window_extent().bounds
            width, height = myfont.size(s)
            # Needs to resize to center
            y += height / 2
            x -= width / 2
        self.surface.blit(font_surface, (x, self.surface.get_height() - y))

    def flipy(self):
        # docstring inherited
        return True

    def get_canvas_width_height(self):
        # docstring inherited
        return 100, 100

    def get_text_width_height_descent(self, s, prop, ismath):
        return 1, 1, 1

    def new_gc(self):
        # docstring inherited
        return GraphicsContextTemplate()

    def points_to_pixels(self, points):
        # if backend doesn't have dpi, e.g., postscript or svg
        return points
        # elif backend assumes a value for pixels_per_inch
        #return points/72.0 * self.dpi.get() * pixels_per_inch/72.0
        # else
        #return points/72.0 * self.dpi.get()


class GraphicsContextTemplate(GraphicsContextBase):
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
        manager.show()



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
    canvas = FigureCanvasTemplate(figure)
    manager = FigureManagerTemplate(canvas, num)
    return manager




class FigureCanvasTemplate(FigureCanvasBase):
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

    def __init__(self, figure=None):
        FigureCanvasBase.__init__(self, figure)

    def draw(self):
        """
        Draw the figure using the renderer.

        It is important that this method actually walk the artist tree
        even if not output is produced because this will trigger
        deferred work (like computing limits auto-limits and tick
        values) that users may want access to before saving to disk.
        """
        renderer = RendererTemplate(self.figure.dpi)
        renderer.surface = self.figure
        self.figure.draw(renderer)

    # You should provide a print_xxx function for every file format
    # you can write.

    # If the file type is not in the base set of filetypes,
    # you should add it to the class-scope filetypes dictionary as follows:
    filetypes = {**FigureCanvasBase.filetypes, 'foo': 'My magic Foo format'}

    def print_foo(self, filename, *args, **kwargs):
        """
        Write out format foo.

        This method is normally called via `.Figure.savefig` and
        `.FigureCanvasBase.print_figure`, which take care of setting the figure
        facecolor, edgecolor, and dpi to the desired output values, and will
        restore them to the original values.  Therefore, `print_foo` does not
        need to handle these settings.
        """
        self.draw()

    def get_default_filetype(self):
        return 'foo'


class FigureManagerTemplate(FigureManagerBase):
    """
    Helper class for pyplot mode, wraps everything up into a neat bundle.

    For non-interactive backends, the base class is sufficient.
    """

    def show(self):
        # do something to display the GUI
        pygame.init()
        main_display = pygame.display.set_mode(self.canvas.figure.get_size())

        FPS = 144
        FramePerSec = pygame.time.Clock()

        self.canvas.figure.canvas.draw()
        main_display.blit(self.canvas.figure, (0, 0))

        show_fig = True
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

FigureCanvas = FigureCanvasTemplate
FigureManager = FigureManagerTemplate
