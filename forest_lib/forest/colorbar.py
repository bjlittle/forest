"""Forest colorbar helpers

A colorbar should re-render as plots update. Since ForestPlot holds
references to matplotlib pcolormesh or imshow return values, a mapping
must be provided between matplotlib.colors.ListedColorMap and a
bokeh.models.ColumnDataSource.

The ColumnDataSource is used as the driving data for bokeh.plotting.Figure
instance call to rect()

.. note:: forest color maps and normalizations are computed in
          forest.util.create_colour_opts() by calling
          matplotlib.colors.from_levels_and_colors()

.. note:: Color map extend "max", "min", "both" can be detected
          through cmap.colorbar_extend which is set by
          matplotlib.colors.from_levels_and_colors()

.. note:: For a BoundaryNorm there is a norm.boundaries property
          which can be used to set figure.rect() widths

.. note:: In the case of extend "min" or "max", a triangle Glyph
          should be added to indicate values outside range

"""
import numpy as np
import bokeh.models
import bokeh.plotting


__all__ = [
    "Colorbar",
    "StaticColorbar",
    "rgb",
    "source_dict",
    "colorbar_figure"
]

class StaticColorbar(object):
    """Colorbar bokeh Div widget serving static images"""
    def __init__(self, app_path, plot_var):
        self.app_path = app_path
        colorbar_link = plot_var + '_colorbar.png'
        colorbar_html = "<img src='" + app_path + "/static/" + \
                        colorbar_link + "'\>"
        self.widget = bokeh.models.widgets.Div(text=colorbar_html,
                                               height=100,
                                               width=800)
    def update(self, current_var):
        """Update static colorbar image"""
        colorbar_link = current_var + '_colorbar.png'
        colorbar_html = "<img src='" + self.app_path + "/static/" + \
                        colorbar_link + "'\>"

        print(colorbar_html)

        try:
            self.widget.text = colorbar_html
        except AttributeError as e1:
            print('Unable to update colorbar as colorbar widget not initiated')

class Colorbar(object):
    """Forest colorbar widget"""
    def __init__(self, color_map, norm, figure=None):
        """Helper to generate a bokeh widget that acts like a colorbar
        """
        if figure is None:
            self.figure = colorbar_figure()
        else:
            self.figure = figure

        # Relationship between data and colors
        source = bokeh.models.ColumnDataSource(source_dict(color_map, norm))
        self.figure.rect(x="x",
                         y=0.5,
                         height=1.,
                         width="width",
                         color="rgb_color",
                         source=source)
        self.source = source

    @property
    def widget(self):
        """To conform to polymorphic Colorbar API expose self.widget"""
        return self.figure


    def update(self, color_map, norm):
        """Re-render colorbar using different color map and limits"""
        self.source.data = source_dict(color_map, norm)
        self.figure.x_range = bokeh.models.Range1d(norm.vmin, norm.vmax)


def source_dict(color_map, norm):
    """Create a ColumnDataSource dict from color map and x range"""
    x = np.linspace(norm.vmin, norm.vmax, color_map.N)
    return {
        "x": x,
        "width": np.full(len(x), x[1] - x[0]),
        "rgb_color": rgb(color_map.colors)
    }


def colorbar_figure():
    """Colorbar bokeh figure with appropriate hover tool"""
    # Make a figure suitable to contain a colorbar
    figure = bokeh.plotting.figure(tools="",
                                   plot_width=500,
                                   plot_height=60)
    figure.yaxis.visible = False
    figure.toolbar_location = None
    figure.min_border = 20

    # Hover tooltip
    hover = bokeh.models.HoverTool()
    hover.tooltips = [
        ("value", "$x"),
        ("color", "$color[hex, swatch]:rgb_color")
    ]
    figure.add_tools(hover)
    return figure


def rgb(colors):
    """Map color map colors to RGB Hexadecimal values"""
    texts = []
    for color in colors:
        if len(color) == 3:
            r, g, b = color
        else:
            r, g, b, _ = color
        text = "#{:02x}{:02x}{:02x}".format(int(255 * r),
                                            int(255 * g),
                                            int(255 * b))
        texts.append(text)
    return texts
