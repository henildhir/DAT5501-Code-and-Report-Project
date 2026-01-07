import unittest
import numpy as np
import pandas as pd
import co2_emissions_forecast as cef

class TestCo2Forecast(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "Country Name": ["United Kingdom", "United Kingdom",
                             "World", "World"],
            "Year": ["2000", "2005", "2000", "2005"],  # strings on purpose
            "CO2 per capita (Trillions)": [1.0, 1.5, 0.5, 0.6],
        })
        # match production behaviour
        self.df["Year"] = pd.to_numeric(self.df["Year"], errors="coerce")

    def test_data_handling_and_types(self):
        # Year must be numeric, no NaN for this sample
        self.assertTrue(np.issubdtype(self.df["Year"].dtype, np.number))
        self.assertFalse(self.df["Year"].isna().any())

    def test_prepare_country_data_output_types(self):
        cd, x_train, y_train = cef.prepare_country_data(self.df, "World")
        # Only requested country
        self.assertTrue((cd["Country Name"] == "World").all())
        # x_train and y_train are 1‑D numeric arrays
        self.assertEqual(x_train.ndim, 1)
        self.assertEqual(y_train.ndim, 1)
        self.assertTrue(np.issubdtype(x_train.dtype, np.number))
        self.assertTrue(np.issubdtype(y_train.dtype, np.number))

    def test_forecasting_reasonable(self):
        _, x_train, y_train = cef.prepare_country_data(self.df, "World")
        degree = cef.get_config()[2]["World"]
        x_fc, y_fc, hist, fut = cef.fit_and_forecast(x_train, y_train, degree)
        # forecast longer than training
        self.assertGreater(len(x_fc), len(x_train))
        # historical / future split around max training year
        max_year = x_train.max()
        self.assertTrue((x_fc[hist] <= max_year).all())
        self.assertTrue((x_fc[fut] >= max_year).all())
        # all forecast values must be finite numbers
        self.assertTrue(np.isfinite(y_fc).all())


if __name__ == "__main__":
    unittest.main()