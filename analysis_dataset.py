import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

gdp = pd.read_csv("World_gdp/new_world_gdp.csv")
population = pd.read_csv("World_population/new_world_population.csv")
co2 = pd.read_csv("World_co2/new_co2_emissions_per_capita.csv")

merged = gdp.merge(population, on=["Country Name","Year"], how="inner")
merged = merged.merge(co2,on=["Country Name","Year"], how="inner")
merged=merged.sort_values(["Country Name", "Year"])

if "Code" in merged.columns:
    merged = merged.drop(columns=["Code"])

merged= merged.rename(columns={"CO2 per capita":"CO2 per capita (Trillions)","Population":"Population (Millions)"})

merged["GDP (Trillions USD($))"]=merged["GDP"]/1e12
merged["Population (Millions)"]=merged["Population (Millions)"]/1e6
merged["GDP per capita"] = (merged["GDP (Trillions USD($))"]*1e6 / merged["Population (Millions)"])

# if "Code" in merged.columns:
#     merged = merged.drop(columns=["Code"])

# if "GDP" in merged.columns:
#     merged=merged.drop(columns=["GDP"])
    
# if "," in merged.columns:
#     merged=merged.drop(columns=[","])

merged = merged.reset_index(drop=True)

print(merged.head())
print(merged.columns)

merged.to_csv("analysis_dataset.csv", index="False")
