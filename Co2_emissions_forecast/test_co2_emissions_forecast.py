import unittest
import pandas as pd
import numpy as np

# Adjust this import according to your .py file name
from co2_emissions_forecast import co2_emissions_forecast  

class TestCO2EmissionsForecast(unittest.TestCase):

    def setUp(self):
        # Create a minimal dataset for testing
        self.test_data = pd.DataFrame({
            "Country Name": ["India"] * 5,
            "Year": [1980, 1985, 1990, 1995, 2000],
            "CO2 per capita (Trillions)": [0.068, 0.074, 0.102, 0.134, 0.18],
            "GDP": [0.068, 0.099, 0.134, 0.178, 0.241],
            "Population (Millions)": [680, 700, 730, 760, 798]
        })

    def test_forecasting_output(self):
        # Call the forecasting function with a DataFrame
        results = co2_emissions_forecast(self.test_data)  
        
        # Check if the output is a dictionary
        self.assertIsInstance(results, dict)

        # Validate that results contain an entry for 'India'
        self.assertIn("India", results)

        # Validate the output for 'India' is a tuple
        india_results = results["India"]
        self.assertIsInstance(india_results, tuple)

        # Ensure the tuple has at least a certain number of elements (adjust according to your expectations)
        self.assertGreaterEqual(len(india_results), 4)  # Example: checking for at least 4 elements

        # Validate that the forecasted CO2 values are numeric
        y_forecast = india_results[3]  # Adjust this index according to your function's output
        self.assertTrue(np.issubdtype(y_forecast.dtype, np.number))

        # Ensure all forecasted values are non-negative
        self.assertTrue(np.all(y_forecast >= 0), "Forecasted CO2 values should be non-negative.")

if __name__ == '__main__':
    unittest.main()