#imports all relevant libraries
import unittest
import pandas as pd
import co2_emissions
import matplotlib.pyplot as plt

class TestAnalysisDatasetDataframe(unittest.TestCase):
    def setUp(self):
        #function sets up a sample dataframe used for validation later on
        self.df = pd.DataFrame( 
            {"Entity": ["India", "India", "United Kingdom"],
                "Code": ["IND", "IND", "GBR"],
                "Year": [1980, 1961, 2008],
                "Annual CO₂ emissions (per capita)": [0.4,0.3,0.12]})

    #cleans all columns in the sample dataframe and checks whether renaming happens correctly
    def test_clean_co2_emissions_filters_and_renames(self):
        #imports value from function in main python file and returns the cleaned dataset
        result = co2_emissions.co2_emissions_cleaning(self.df)


        #checks for both cases where years are 1980 and later to ensure data is in the valid time range
        self.assertTrue((result["Year"] >= 1980).all())
        #confirms whether data before 1980 is not included as this is outside the intended time range from 1980-2024
        self.assertNotIn(1979, result["Year"].values)

        #confirms whether all column headers are the same as provided to ensure less chance of errors and overriding different columns
        self.assertIn("Country Name", result.columns)
        self.assertIn("CO2 per capita", result.columns)
        self.assertNotIn("Entity", result.columns)
        self.assertNotIn("Annual CO₂ emissions (per capita)", result.columns)

        #check values for 1980 India to confirm intended nation used for the analysis
        row_1980 = result[result["Year"] == 1980].iloc[0]
        self.assertEqual(row_1980["Country Name"], "India")
        self.assertAlmostEqual(row_1980["CO2 per capita"], 0.4)

if __name__ == "__main__":
    unittest.main()