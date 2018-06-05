import unittest
import bokeh.models.widgets
import forest.plot


class TestForestPlot(unittest.TestCase):
    def test_create_colorbar_widget(self):
        fixture = self.make_forest_plot()
        result = fixture.create_colorbar_widget()
        self.assert_div_has(result,
            text="<img src='fake/app/path/static/fake_plot_var_colorbar.png'\>",
            height=100,
            width=800)

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