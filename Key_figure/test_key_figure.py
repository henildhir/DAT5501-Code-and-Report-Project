import unittest
import pandas as pd
import key_figure
import matplotlib.pyplot as plt


class TestAnalysisDatasetDataframe(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame(
            {
                "Country Name": ["India", "India", "United Kingdom"],
                "Year": [1980, 1981, 1980],
                "CO2 per capita (Trillions)": [0.18, 0.19, 0.40],
                "GDP": [1.0, 1.1, 5.0],  # extra column, not needed by plot
            }
        )

    def test_sample_data_structure_and_dtypes(self):
        required = ["Country Name", "Year", "CO2 per capita (Trillions)"]

        for col in required:
            self.assertIn(col, self.df.columns)

        self.assertTrue(pd.api.types.is_integer_dtype(self.df["Year"]))
        self.assertTrue(
            pd.api.types.is_numeric_dtype(
                self.df["CO2 per capita (Trillions)"]
            )
        )
        self.assertTrue(
            pd.api.types.is_object_dtype(self.df["Country Name"])
            or pd.api.types.is_string_dtype(self.df["Country Name"])
        )

        self.assertFalse(self.df[required].isnull().values.any())

    def test_column_dtypes_are_correct(self):
        year_col = self.df["Year"]
        co2_col = self.df["CO2 per capita (Trillions)"]
        country_col = self.df["Country Name"]

        # Year should be integer-like
        self.assertTrue(
            pd.api.types.is_integer_dtype(year_col),
            msg="Year column should be integer dtype.",
        )

        # CO2 per capita should be numeric (int or float)
        self.assertTrue(
            pd.api.types.is_numeric_dtype(co2_col),
            msg="CO2 per capita column should be numeric.",
        )

        # Country Name should be string / object
        self.assertTrue(
            pd.api.types.is_object_dtype(country_col)
            or pd.api.types.is_string_dtype(country_col),
            msg="Country Name column should be string/object dtype.",
        )

if __name__ == "__main__":
    unittest.main()