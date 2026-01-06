import unittest
import pandas as pd
import numpy as np
import matplotlib

# avoid GUI popups during tests
matplotlib.use("Agg")

import co2_emissions_gdp_per_capita as cg   # adjust if module name differs


class TestCo2EmissionsGdpPerCapita(unittest.TestCase):
    def setUp(self):
        """
        Small dataframe with a known pattern:
        - 1 missing Country Name
        - 1 missing CO2 value
        - 1 missing GDP value
        - no missing Year
        """
        self.sample_data = pd.DataFrame(
            {
                "Country Name": ["World", "World", None, "India"],
                "Year": [2010, 2011, 2012, 2010],
                "CO2 per capita (Trillions)": [5.0, 5.5, 6.0, np.nan],
                "GDP per capita": [10000.0, np.nan, 12000.0, 2000.0],
            }
        )

    def test_columns_present(self):
        """Check that the key columns exist."""
        expected = {
            "Country Name",
            "Year",
            "CO2 per capita (Trillions)",
            "GDP per capita",
        }
        self.assertTrue(expected.issubset(self.sample_data.columns))

    def test_null_values_exist_in_expected_columns(self):
        """
        Important null checks:
        - there are some nulls in the dataframe,
        - each of the three columns we know has exactly one null,
        - 'Year' has no nulls.
        """
        # At least one null overall
        self.assertTrue(self.sample_data.isnull().values.any())

        # Per‑column expectations
        null_counts = self.sample_data.isnull().sum()
        self.assertEqual(null_counts["Country Name"], 1)
        self.assertEqual(null_counts["CO2 per capita (Trillions)"], 1)
        self.assertEqual(null_counts["GDP per capita"], 1)
        self.assertEqual(null_counts["Year"], 0)

    def test_no_nulls_in_numeric_columns_real_dataset(self):
        """
        Simple but important: load the real CSV and check that the
        critical numeric columns have no missing values.
        (Change expectation if your real data *should* contain nulls.)
        """
        dataset = pd.read_csv("analysis_dataset.csv")

        for col in ["Year", "GDP per capita", "CO2 per capita (Trillions)"]:
            self.assertFalse(
                dataset[col].isnull().any(),
                msg=f"Found nulls in real dataset column: {col}",
            )


if __name__ == "__main__":
    unittest.main()