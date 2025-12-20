import pandas as pd

world_population = pd.read_csv("World_population/world_population.csv", skiprows=4)

countries=["United Kingdom","India","Malawi","World"]
world_population_filtered = world_population[world_population["Country Name"].isin(countries)]

year_cols = [c for c in world_population.columns if c.isdigit() and int(c) >=1980]

world_population_filtered = world_population_filtered[["Country Name"] + year_cols]

world_population_long = world_population_filtered.melt(
    id_vars="Country Name",
    value_vars=year_cols,
    var_name="Year",
    value_name="Population"
)

world_population_long = world_population_long.sort_values(
    by=["Country Name", "Year"],
    ascending=[True, True]
)

world_population_long["Year"] = world_population_long["Year"].astype(int)

print(world_population_long.head())

world_population_long.to_csv("World_population/new_world_population.csv",index = False)