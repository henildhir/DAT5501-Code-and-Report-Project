import unittest
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Optional: avoid GUI popups during tests

import annual_percentage_change as ac  # adjust to your module name

class TestAnnualPercentChange(unittest.TestCase):

    def setUp(self):
        self.sample_data = pd.DataFrame({
            "Country Name": ["World", "World", "World", "CountryA", "CountryA"],
            "Year": [2000, 2001, 2002, 2000, 2001],
            "CO2 per capita (Trillions)": [1.0, 1.1, 1.2, 0, 0],
            "GDP per capita": [1000, 1100, 1210, 500, 0]
        })

    def test_filter_and_calculate_percentage_change(self):
        countries = ["World"]
        result = ac.filter_and_calculate(self.sample_data, countries)

        # Only rows in result must have countries we asked for
        self.assertTrue(result["Country Name"].isin(countries).all())

        # Percentage changes: first row per country is NaN
        first_idx = result.index[0]
        self.assertTrue(np.isnan(result.loc[first_idx, "CO2_percentage_change"]))
        self.assertTrue(np.isnan(result.loc[first_idx, "GDP_percentage_change"]))

        # Second row has ~10% change for World
        self.assertAlmostEqual(result.loc[first_idx+1, "CO2_percentage_change"], 10.0, places=2)
        self.assertAlmostEqual(result.loc[first_idx+1, "GDP_percentage_change"], 10.0, places=2)

    def test_handle_zero_and_constant_values(self):
        countries = ["CountryA"]
        result = ac.filter_and_calculate(self.sample_data, countries)

        # Since CO2 is constant zero for CountryA, pct_change returns NaN or Inf
        # Ensure pct_change returns expected NaN on first row, and check second row behavior
        first_idx = result.index[0]
        self.assertTrue(np.isnan(result.loc[first_idx, "CO2_percentage_change"]))

        # The rest can be NaN, Inf, or -Inf because of zeros - check if they’re recognized as numeric but invalid
        col = result["CO2_percentage_change"].iloc[1]
        self.assertTrue(np.isnan(col) or np.isinf(col))

    def test_create_plot_structure(self):
        countries = ["World", "CountryA"]
        data = ac.filter_and_calculate(self.sample_data, countries)
        fig, ax = ac.create_plots(data, countries)
        
        # Assert figure and axes created as expected
        self.assertEqual(len(ax), 2)
        self.assertTrue(hasattr(fig, "savefig"))

        # Basic labels presence checks (string contains)
        self.assertIn("Year", ax[0].get_xlabel())
        self.assertIn("% change", ax[0].get_ylabel())
        self.assertIn("Year", ax[1].get_xlabel())
        self.assertIn("% change", ax[1].get_ylabel())

if __name__ == "__main__":
    unittest.main()