import unittest
import pandas as pd
import co2_emissions
import matplotlib.pyplot as plt

class TestAnalysisDatasetDataframe(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame(
            {
                "Entity": ["India", "India", "United Kingdom"],
                "Code": ["IND", "IND", "GBR"],
                "Year": [1980, 1961, 2008],
                "Annual CO₂ emissions (per capita)": [0.4,0.3,0.12]
            }
        )

    def test_clean_co2_emissions_filters_and_renames(self):
        result = co2_emissions.co2_emissions_cleaning(self.df)

        # Only years >= 1980
        self.assertTrue((result["Year"] >= 1980).all())
        self.assertNotIn(1979, result["Year"].values)

        # Columns renamed correctly
        self.assertIn("Country Name", result.columns)
        self.assertIn("CO2 per capita", result.columns)
        self.assertNotIn("Entity", result.columns)
        self.assertNotIn("Annual CO₂ emissions (per capita)", result.columns)

        # Check values for 1980 India
        row_1980 = result[result["Year"] == 1980].iloc[0]
        self.assertEqual(row_1980["Country Name"], "India")
        self.assertAlmostEqual(row_1980["CO2 per capita"], 0.4)

if __name__ == "__main__":
    unittest.main()