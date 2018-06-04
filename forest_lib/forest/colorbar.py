"""Forest colorbar helpers

A colorbar should re-render as plots update. Since ForestPlot holds
references to matplotlib pcolormesh or imshow return values, a mapping
must be provided between matplotlib.colors.ListedColorMap and a
bokeh.models.ColumnDataSource.

The ColumnDataSource is used as the driving data for bokeh.plotting.Figure
instance call to rect()
"""


def colorbar(color_map):
    """Helper to generate a bokeh widget that acts like a colorbar"""
    # Make a figure suitable to contain a colorbar
    figure = bokeh.plotting.figure()
    figure.yaxis.visible = False
    figure.toolbar_location = None
    figure.min_border = 20

    # Relationship between data and colors
    x = np.linspace(x_min, x_max, color_map.N)
    width = x[1] - x[0]
    rgb_colors = rgb(color_map.colors)
    figure.rect(x=x, y=0.5, height=1., width=width,
                color=rgb_colors)

    # Hover tooltip
    hover = bokeh.models.HoverTool()
    hover.tooltips = [
        ("value", "$value"),
        ("color", "$color[hex, swatch]:fill_color")
    ]
    figure.add_tools(hover)
    return figure


def rgb(colors):
    """Map color map colors to RGB Hexadecimal values"""
    return ["#{:02x}{:02x}{:02x}".format(int(255 * r), int(255 * g), int(255 * b))
            for r, g, b in colors]
