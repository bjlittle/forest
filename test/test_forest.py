import unittest
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import bokeh.models
import bokeh.models.widgets
import forest.plot


class TestMatplotlibAPI(unittest.TestCase):
    def test_get_cmap(self):
        """matplotlib color map API"""
        x, y = np.linspace(0, 1, 100), np.linspace(0, 1, 100)
        X, Y = np.meshgrid(x, y)
        Z = X + Y
        quad_mesh = plt.pcolormesh(X, Y, Z)
        color_map = quad_mesh.get_cmap()
        self.assertEqual(color_map.N, 256)
        self.assertEqual(np.shape(color_map.colors), (256, 3))
        print(quad_mesh.norm(Z.max()))
        v = np.linspace(Z.min(), Z.max(), color_map.N,
                        endpoint=False)
        self.assertAlmostEqual(quad_mesh.norm.vmin, v.min())
        self.assertAlmostEqual(quad_mesh.norm.vmax, v.max())


class TestForestColorbar(unittest.TestCase):
    """
    Forest colorbars use a figure.rect() GlyphRenderer to
    observe a ColumnDataSource containing colors plucked
    from a matplotlib.colors.LinerSegmentedColormap

    .. note:: The builtin bokeh.models.ColorBar that uses
              a bokeh.models.LinearColorMapper is unsuited
              to the general colorschemes used by Forest
    """
    def test_colorbar_figure(self):
        """colorbar figure should be short, wide and have limited tools"""
        figure = forest.colorbar_figure()
        self.assertEqual(figure.plot_height, 60)
        self.assertEqual(figure.plot_width, 500)
        self.assertEqual(figure.toolbar_location, None)
        self.assertEqual(figure.yaxis[0].visible, False)
        self.assertIsInstance(figure.tools[0], bokeh.models.HoverTool)

    def test_create_colorbar_returns_bokeh_figure(self):
        forest_plot = self.make_forest_plot()
        forest_plot.create_colorbar()
        self.assertIsInstance(forest_plot.colorbar_source,
                              bokeh.models.ColumnDataSource)
        self.assertIsInstance(forest_plot.colorbar_figure,
                              bokeh.plotting.Figure)

    @unittest.skip("deprecated feature")
    def test_create_colorbar_widget(self):
        fixture = self.make_forest_plot()
        result = fixture.create_colorbar_widget()
        self.assert_div_has(result,
            text="<img src='fake/app/path/static/fake_plot_var_colorbar.png'\>",
            height=100,
            width=800)

    @unittest.skip("deprecated feature")
    def test_update_colorbar_widget(self):
        """
        .. note:: update_colorbar_widget() is only called by
                  set_var() which sets current_var
        """
        fixture = self.make_forest_plot()
        fixture.create_colorbar_widget()
        fixture.current_var = "current_var"  # simulate set_var()
        fixture.update_colorbar_widget()
        self.assertEqual(fixture.colorbar_widget.text,
            "<img src='fake/app/path/static/current_var_colorbar.png'\>")

    def make_forest_plot(self):
        # Model configuration details
        fake_config = "config"
        dataset = {fake_config: {"data_type_name": None}}
        conf1 = fake_config

        # Region details
        fake_region = "region"
        reg1 = fake_region
        rd1 = {fake_region: None}

        # Settings needed by create_colorbar_widget
        plot_var = "fake_plot_var"
        app_path = "fake/app/path"

        model_run_time = None
        po1 = None
        figname = None
        unit_dict = None
        unit_dict_display = None
        init_time = None
        return forest.plot.ForestPlot(dataset,
                                      model_run_time,
                                      po1,
                                      figname,
                                      plot_var,
                                      conf1,
                                      reg1,
                                      rd1,
                                      unit_dict,
                                      unit_dict_display,
                                      app_path,
                                      init_time)

    def assert_div_has(self, div, text, width, height):
        self.assertIsInstance(div, bokeh.models.widgets.Div)
        self.assertEqual(div.text, text)
        self.assertEqual(div.height, height)
        self.assertEqual(div.width, width)
