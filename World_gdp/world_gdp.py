import pandas as pd

world_gdp = pd.read_csv("World_gdp/world_gdp.csv", skiprows=4)
countries =["United Kingdom","India","Malawi","World"]
world_gdp_filtered=world_gdp[world_gdp["Country Name"].isin(countries)]

year_cols = [c for c in world_gdp_filtered.columns if c.isdigit() and int(c) >= 1980]
world_gdp_filtered=world_gdp_filtered[["Country Name"]+year_cols]

world_gdp_long = world_gdp_filtered.melt(
    id_vars="Country Name",
    value_vars=year_cols,
    var_name="Year",
    value_name="GDP"
)

world_gdp_long = world_gdp_long.sort_values(
    by=["Country Name", "Year"],
    ascending=[True, True]
)

world_gdp_long["Year"] = world_gdp_long["Year"].astype(int)

world_gdp_long.to_csv(
    "World_gdp/new_world_gdp.csv",
    index=False  # this avoids saving the 0,1,2 index column
)

print(world_gdp_long.head())