#all relevant libraries imported
import unittest
import pandas as pd

class TestAnalysisDatasetDataframe(unittest.TestCase):
    def setUp(self):
        #function sets up a sample dataframe used for validation later on with similar column names
        self.df = pd.DataFrame(
            {"Country Name": ["India", "India", "United Kingdom"],
                "Year": [1980, 1981, 1980],
                "CO2 per capita (Trillions)": [0.18, 0.19, 0.40],
                "GDP": [1.0, 1.1, 5.0],})

    def test_required_columns_present_and_count(self):
        #check that required columns exist and count columns of data for fewer errors and consistency
        required = ["Year", "Country Name", "CO2 per capita (Trillions)"]

        #checks whether all required columns present for consistency
        for col in required:
            self.assertIn(col, self.df.columns)

        #checks whether the sample dataframe has greater than equal to 1 column headers as this is the minimum required to plot a graph
        self.assertGreaterEqual(self.df.shape[1], len(required))

    def test_column_dtypes_are_correct(self):
        #check that: year values are integers, co2 per capita values are numeric country name values are strings for consistency
        year_col = self.df["Year"]
        co2_col = self.df["CO2 per capita (Trillions)"]
        country_col = self.df["Country Name"]

        #checks whether year column contains integers for consistency and reduced errors and print a suitable message
        self.assertTrue(
            pd.api.types.is_integer_dtype(year_col),
            msg="Year column should be integer dtype.",)

        #checks whether co2 column contains integers or floats for consistency and reduced errors and print a suitable message
        self.assertTrue(
            pd.api.types.is_numeric_dtype(co2_col),
            msg="CO2 per capita column should be numeric.",)

        #checks whether country column contains integers for consistency and reduced errors and print a suitable message
        self.assertTrue(
            pd.api.types.is_object_dtype(country_col)
            or pd.api.types.is_string_dtype(country_col),
            msg="Country Name column should be string/object dtype.",)

if __name__ == "__main__":
    unittest.main()