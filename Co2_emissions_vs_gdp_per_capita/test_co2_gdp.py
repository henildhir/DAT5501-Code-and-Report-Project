#imports all libraries and functions required 
import unittest
import pandas as pd
import numpy as np
import co2_emissions_gdp_per_capita as cg 

class TestCo2GdpRegression(unittest.TestCase):
    def setUp(self):
        #function sets up a sample dataframe used for validation later on
        self.sample = pd.DataFrame({
            "Country Name": ["World", "World", "World", "Other", "Other"],
            "Year": [2000, 2005, 2010, 2005, 2010],
            "GDP per capita":                [1000, 2000, 3000, 1500, 2500],
            "CO2 per capita (Trillions)":    [1.0, 2.0, 3.0, 0.5, 0.7],
        })

    #tests data for the previous years with correct array and datatype
    def test_filter_10_years_data_handling(self):
        filter_df, min_year, max_year = cg.filter_10_years(self.sample)

        self.assertTrue(np.issubdtype(filter_df["Year"].dtype, np.number))
        self.assertEqual(max_year, self.sample["Year"].max())
        self.assertEqual(min_year, max_year - 9)

        #Row with Year 2000 should be removed
        self.assertFalse((filter_df["Year"] == 2000).any())

    #tests x and y values in the select function of original python file
    def test_select_world_returns_correct_arrays(self):
        x, y = cg.select(self.sample)
        self.assertEqual(len(x), 3)
        self.assertEqual(len(y), 3)

        #tests whether the column values are equal to country given and compares both x and y values
        self.assertTrue((self.sample.loc[self.sample["Country Name"]=="World","GDP per capita"].values == x).all())
        self.assertTrue((self.sample.loc[self.sample["Country Name"]=="World","CO2 per capita (Trillions)"].values == y).all())

    #tests values given in sample dataset and calculates regression statistics
    def test_regression_values_reasonable(self):
        x, y = cg.select(self.sample)
        r, x_grid, y_hat, ci_lower, ci_upper = cg.regression(x, y)
        self.assertAlmostEqual(abs(r), 1.0, places=4)
        self.assertEqual(len(x_grid), len(y_hat))
        
        #calculates confidence interval for upper and lower bound for given data values and compares it to numpy array
        self.assertEqual(len(x_grid), len(ci_lower))
        self.assertEqual(len(x_grid), len(ci_upper))
        self.assertTrue(np.isfinite(y_hat).all())
        self.assertTrue(np.isfinite(ci_lower).all())
        self.assertTrue(np.isfinite(ci_upper).all())

if __name__ == "__main__":
    unittest.main()