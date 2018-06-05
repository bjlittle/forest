import unittest
import bokeh.models.widgets
import forest.plot


class TestForestPlot(unittest.TestCase):
    def test_colorbar_support(self):
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
        fixture = forest.plot.ForestPlot(dataset,
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
        result = fixture.create_colorbar_widget()
        self.assertIsInstance(result, bokeh.models.widgets.Div)
        self.assertEqual(result.text,
                "<img src='fake/app/path/static/fake_plot_var_colorbar.png'\>")
        self.assertEqual(result.height, 100)
        self.assertEqual(result.width, 800)
