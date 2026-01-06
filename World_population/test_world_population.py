import unittest
import pandas as pd
import world_population   # your module name

class TestWorldPopulation(unittest.TestCase):

    def setUp(self):
        # Premade dataframe in the *same shape* as the real CSV after skiprows
        self.df = pd.DataFrame(
            {
                "Country Name": ["India", "India", "Brazil"],
                "Country Code": ["IND", "IND", "BRA"],
                "Indicator Name": ["Population, total"] * 3,
                "Indicator Code": ["SP.POP.TOTL"] * 3,
                "1979": [650_000_000, 651_000_000, 120_000_000],
                "1980": [660_000_000, 661_000_000, 121_000_000],
                "1981": [670_000_000, 671_000_000, 122_000_000],
            }
        )

    def test_filter_and_convert_to_long(self):
        world_population_filtered = world_population.filter(self.df)

        # only "India" should remain (Brazil is not in the countries list)
        self.assertTrue(
            (world_population_filtered["Country Name"].unique() == ["India"]).all()
        )

        # only selects the year column and filters for values that are 1980 or after
        self.assertNotIn("1979", world_population_filtered.columns)
        self.assertIn("1980", world_population_filtered.columns)
        self.assertIn("1981", world_population_filtered.columns)

        # converts from wide format to long format
        world_population_long = world_population.convert_to_long(world_population_filtered)

        # checks that the correct columns exist
        self.assertCountEqual(
            world_population_long.columns.tolist(),
            ["Country Name", "Year", "Population"],
        )

        # number of rows = rows in filtered * number of year columns (2: 1980, 1981)
        num_rows_filtered = len(world_population_filtered)      # 2 India rows
        num_year_cols = 2                                      # 1980, 1981
        expected_rows = num_rows_filtered * num_year_cols      # 2 * 2 = 4
        self.assertEqual(len(world_population_long), expected_rows)

    def test_sort_and_fix_types(self):
        # applies the same pipeline steps as in the script
        world_population_filtered = world_population.filter(self.df)
        world_population_long = world_population.convert_to_long(world_population_filtered)
        world_population_long = world_population.sort_and_fix(world_population_long)

        # validates datatype in year column to ensure all data values are integers
        self.assertTrue(pd.api.types.is_integer_dtype(world_population_long["Year"]))

        # Population should be numeric
        self.assertTrue(pd.api.types.is_numeric_dtype(world_population_long["Population"]))

        # verifies the data is sorted by Country Name and Year
        sorted_copy = world_population_long.sort_values(
            by=["Country Name", "Year"], ascending=[True, True]
        )
        self.assertTrue(
            world_population_long.reset_index(drop=True).equals(
                sorted_copy.reset_index(drop=True)
            )
        )

if __name__ == "__main__":
    unittest.main()