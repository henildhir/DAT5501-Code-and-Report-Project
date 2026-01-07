import unittest
import pandas as pd
import numpy as np

import co2_emissions_gdp_per_capita as cg 

class TestCo2GdpRegression(unittest.TestCase):

    def setUp(self):
        #Sample data with two countries and simple linear relation for World
        self.sample = pd.DataFrame({
            "Country Name": ["World", "World", "World", "Other", "Other"],
            "Year": [2000, 2005, 2010, 2005, 2010],
            "GDP per capita":                [1000, 2000, 3000, 1500, 2500],
            "CO2 per capita (Trillions)":    [1.0, 2.0, 3.0, 0.5, 0.7],
        })

    def test_filter_10_years_data_handling(self):
        #Ensure Year is numeric and filtering selects last 10 years correctly
        #Pretend max year is 2010 -> last 10 years: 2001–2010, so 2000 should drop
        filter_df, min_year, max_year = cg.filter_10_years(self.sample)

        self.assertTrue(np.issubdtype(filter_df["Year"].dtype, np.number))
        self.assertEqual(max_year, self.sample["Year"].max())
        self.assertEqual(min_year, max_year - 9)

        #Row with Year 2000 should be removed
        self.assertFalse((filter_df["Year"] == 2000).any())

    def test_select_world_returns_correct_arrays(self):
        x, y = cg.select(self.sample)

        #Only rows for World
        self.assertEqual(len(x), 3)
        self.assertEqual(len(y), 3)
        self.assertTrue((self.sample.loc[self.sample["Country Name"]=="World",
                                         "GDP per capita"].values == x).all())
        self.assertTrue((self.sample.loc[self.sample["Country Name"]=="World",
                                         "CO2 per capita (Trillions)"].values == y).all())

    def test_regression_values_reasonable(self):
        x, y = cg.select(self.sample)
        r, x_grid, y_hat, ci_lower, ci_upper = cg.regression(x, y)

        #Since y = 0.001*x here (perfect linear), |r| should be close to 1
        self.assertAlmostEqual(abs(r), 1.0, places=4)

        #Regression outputs must all have same length and be finite
        self.assertEqual(len(x_grid), len(y_hat))
        self.assertEqual(len(x_grid), len(ci_lower))
        self.assertEqual(len(x_grid), len(ci_upper))
        self.assertTrue(np.isfinite(y_hat).all())
        self.assertTrue(np.isfinite(ci_lower).all())
        self.assertTrue(np.isfinite(ci_upper).all())


if __name__ == "__main__":
    unittest.main()