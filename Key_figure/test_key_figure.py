import unittest
import pandas as pd
import key_figure
import matplotlib.pyplot as plt

class TestAnalysisDatasetDataframe(unittest.TestCase):
    #function sets up a sample dataframe used for validation later on
    def setUp(self):
        self.df = pd.DataFrame(
            {"Country Name": ["India", "India", "United Kingdom"],
                "Year": [1980, 1981, 1980],
                "CO2 per capita (Trillions)": [0.18, 0.19, 0.40],
                "GDP": [1.0, 1.1, 5.0],})

    #checks all columns and all datatypes to ensure no values are different types
    def test_sample_data_structure_and_dtypes(self):
        required = ["Country Name", "Year", "CO2 per capita (Trillions)"]
        #checks whether there is a value within the column to ensure consistency
        for col in required:
            self.assertIn(col, self.df.columns)

        #checks all valyes within the given column to ensure consistency throughout 
        self.assertTrue(pd.api.types.is_integer_dtype(self.df["Year"]))
        #returns true if the values within the column are numeric data types to ensure consistency 
        self.assertTrue(
            pd.api.types.is_numeric_dtype(
                self.df["CO2 per capita (Trillions)"]))
        #returns true if the values within the columns are either an object or a string data types to ensure consistency
        self.assertTrue(
            pd.api.types.is_object_dtype(self.df["Country Name"])
            or pd.api.types.is_string_dtype(self.df["Country Name"]))
        self.assertFalse(self.df[required].isnull().values.any())

    #checks whether all datatypes are correct by using sample dataset to ensure consistency when
    def test_column_dtypes_are_correct(self):
        year_col = self.df["Year"]
        co2_col = self.df["CO2 per capita (Trillions)"]
        country_col = self.df["Country Name"]

        #year column should be only be integer for consistency and returns a message if false is returned
        self.assertTrue(
            pd.api.types.is_integer_dtype(year_col),
            msg="Year column should be integer dtype.",)

        #co2 column should be numeric (integers) for consistency and returns a message if false is returned
        self.assertTrue(
            pd.api.types.is_numeric_dtype(co2_col),
            msg="CO2 per capita column should be numeric.",)

        #country Name should be string / object for consistency and returns a message if false is returned
        self.assertTrue(
            pd.api.types.is_object_dtype(country_col)
            or pd.api.types.is_string_dtype(country_col),
            msg="Country Name column should be string/object dtype.",)

if __name__ == "__main__":
    unittest.main()