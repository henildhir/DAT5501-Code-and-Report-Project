#imports all necessary libraries 
import unittest
import numpy as np
import pandas as pd
import co2_emissions_forecast as cef

class TestCo2Forecast(unittest.TestCase):
    #a sample dataframe created to check for validation and values to be passed onto other tests
    def setUp(self):
        self.df = pd.DataFrame({
            "Country Name": ["United Kingdom", "United Kingdom",
                             "World", "World"],
            "Year": ["2000", "2005", "2000", "2005"],
            "CO2 per capita (Trillions)": [1.0, 1.5, 0.5, 0.6],
        })
        #converts year column to numeric values to ensure consistency and no string values are in the column
        self.df["Year"] = pd.to_numeric(self.df["Year"], errors="coerce")

    #tests year column for any integers and if all data values are integers
    def test_data_handling_and_types(self):
        self.assertTrue(np.issubdtype(self.df["Year"].dtype, np.number))
        self.assertFalse(self.df["Year"].isna().any())

    #takes in a country and performs x train and y train and outputs a numpy array
    def test_prepare_country_data_output_types(self):
        cd, x_train, y_train = cef.prepare_country_data(self.df, "World")
        self.assertTrue((cd["Country Name"] == "World").all())

        #tests whether both x and y numpy arrays are 1 dimension
        self.assertEqual(x_train.ndim, 1)
        self.assertEqual(y_train.ndim, 1)
        self.assertTrue(np.issubdtype(x_train.dtype, np.number))
        self.assertTrue(np.issubdtype(y_train.dtype, np.number))

    #takes in 'world' as test unit with degree of 2 and checks all forecasting outputs
    def test_forecasting(self):
        _, x_train, y_train = cef.prepare_country_data(self.df, "World")
        degree = cef.get_config()[2]["World"]
        x_fc, y_fc, hist, fut = cef.fit_and_forecast(x_train, y_train, degree)
        # forecast longer than training
        self.assertGreater(len(x_fc), len(x_train))
        # historical / future split around max training year
        max_year = x_train.max()
        #checks whether historcal and future forecasts are below the max year and above max year respectively
        self.assertTrue((x_fc[hist] <= max_year).all())
        self.assertTrue((x_fc[fut] >= max_year).all())
        # all forecast values must be finite numbers
        self.assertTrue(np.isfinite(y_fc).all())

if __name__ == "__main__":
    unittest.main()