import pandas as pd

co2_emissions=pd.read_csv("World_co2/co2-emissions-per-capita.csv")

co2_emissions=co2_emissions[co2_emissions["Year"] >= 1980]

co2_emissions=co2_emissions.rename(
    columns = {
        "Entity":"Country Name",
        "Annual CO₂ emissions (per capita)":"CO2 per capita",
    }
)

print(co2_emissions.head())

co2_emissions.to_csv("World_co2/new_co2_emissions_per_capita.csv",index=False)