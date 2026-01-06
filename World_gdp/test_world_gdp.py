import unittest
import pandas as pd
import world_gdp

class TestWorldGDP(unittest.TestCase):
    def setUp(self):
        # Minimal synthetic dataset in the same *shape* as the real one
        self.df = pd.DataFrame(
            {
                "Country Name": ["India", "India", "Brazil"],
                "Country Code": ["IND", "IND", "BRA"],
                "Indicator Name": ["GDP (current US$)"] * 3,
                "Indicator Code": ["NY.GDP.MKTP.CD"] * 3,
                "1979": [100.0, 200.0, 300.0],
                "1980": [110.0, 210.0, 310.0],
                "1981": [120.0, 220.0, 320.0],
            }
        )

    def test_filter_and_convert_to_long(self):
        # filter selected countries and years >= 1980
        filtered = world_gdp.filter(self.df)

        # only specified countries should remain (India is in list, Brazil is not)
        self.assertTrue((filtered["Country Name"].unique() == ["India"]).all())

        # correct year columns kept
        self.assertNotIn("1979", filtered.columns)
        self.assertIn("1980", filtered.columns)
        self.assertIn("1981", filtered.columns)

        # convert to long
        long_df = world_gdp.convert_to_long(filtered)

        # columns should be exactly these three (order not important in assert)
        self.assertCountEqual(long_df.columns.tolist(), ["Country Name", "Year", "GDP"])

        # number of rows = countries_after_filter * number_of_year_columns
        num_countries_rows = len(filtered)            # here: 2 India rows
        num_year_cols = 2                             # 1980, 1981
        expected_rows = num_countries_rows * num_year_cols  # 2 * 2 = 4
        self.assertEqual(len(long_df), expected_rows)

    def test_sort_and_fix_types(self):
        filtered = world_gdp.filter(self.df)
        long_df = world_gdp.convert_to_long(filtered)
        clean_df = world_gdp.sort_and_fix(long_df)

        # Year should be integer dtype
        self.assertTrue(pd.api.types.is_integer_dtype(clean_df["Year"]))

        # GDP should be numeric dtype
        self.assertTrue(pd.api.types.is_numeric_dtype(clean_df["GDP"]))

        # Data should be sorted by Country Name then Year
        sorted_copy = clean_df.sort_values(["Country Name", "Year"], ascending=[True, True])
        self.assertTrue(
            clean_df.reset_index(drop=True).equals(sorted_copy.reset_index(drop=True))
        )


if __name__ == "__main__":
    unittest.main()