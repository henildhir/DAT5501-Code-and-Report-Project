#imports all relevant libraries
import unittest
import pandas as pd
import world_gdp

class TestWorldGDP(unittest.TestCase):
    def setUp(self):
        #function sets up a sample dataframe used for validation later on with similar column
        self.df = pd.DataFrame(
            {"Country Name": ["India", "India", "Brazil"],
                "Country Code": ["IND", "IND", "BRA"],
                "Indicator Name": ["GDP (current US$)"] * 3,
                "Indicator Code": ["NY.GDP.MKTP.CD"] * 3,
                "1979": [100.0, 200.0, 300.0],
                "1980": [110.0, 210.0, 310.0],
                "1981": [120.0, 220.0, 320.0],})

    #tests the filtered dataset and converts to long format for easier plotting
    def test_filter_and_convert_to_long(self):
        #imports the world_gdp function from main python file for analysis and returns the filtered dataset
        filtered = world_gdp.filter(self.df)

        #only specified countries should remain (India is in list, Brazil is not) to ensure all correct entities/nations are used for analysis
        self.assertTrue((filtered["Country Name"].unique() == ["India"]).all())

        #checks for whether the intended years are within the dataset. Time-range is between 1980 and 2024 therefore it also checks for years before 1980
        self.assertNotIn("1979", filtered.columns)
        self.assertIn("1980", filtered.columns)
        self.assertIn("1981", filtered.columns)

        #convert to long format for easier access and data reading, ensures there are no errors
        long_df = world_gdp.convert_to_long(filtered)

        #columns should be exactly these three to maintain consistency and to ensure graphs produce contain only these values
        self.assertCountEqual(long_df.columns.tolist(), ["Country Name", "Year", "GDP"])

        #number of rows = countries_after_filter * number_of_year_columns 
        num_countries_rows = len(filtered)            # here: 2 India rows
        num_year_cols = 2                             # 1980, 1981
        expected_rows = num_countries_rows * num_year_cols  # 2 * 2 = 4
        #checks whether the required length of array is the same as expected rows
        self.assertEqual(len(long_df), expected_rows)

    #tests for sorting, converting and filtering the sub sample by importing filter(),convert_to_long and sort functions from main python file for analysis
    def test_sort_and_fix_types(self):
        filtered = world_gdp.filter(self.df)
        long_df = world_gdp.convert_to_long(filtered)
        clean_df = world_gdp.sort_and_fix(long_df)

        #checks whether values within year column are integers to ensure consistency
        self.assertTrue(pd.api.types.is_integer_dtype(clean_df["Year"]))

        #checks whether values within year column are integers to ensure consistency
        self.assertTrue(pd.api.types.is_numeric_dtype(clean_df["GDP"]))

        #Data should be sorted by Country Name then Year to improve readability
        sorted_copy = clean_df.sort_values(["Country Name", "Year"], ascending=[True, True])
        self.assertTrue(
            clean_df.reset_index(drop=True).equals(sorted_copy.reset_index(drop=True))
        )


if __name__ == "__main__":
    unittest.main()