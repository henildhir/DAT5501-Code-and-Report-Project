#imports relevants functions used within this file
import pandas as pd

def load():
    #uses pandas to read csv file and skips first 4 rows as they do not contain any data
    world_population = pd.read_csv("World_population/world_population.csv", skiprows=4)
    return world_population

def filter(world_population):
    #filters out the desired countries given within the countries list
    countries=["United Kingdom","India","Malawi","World"]
    world_population_filtered = world_population[world_population["Country Name"].isin(countries)]

    #only selectes the year column and filters for values that are 1980 or after
    year_cols = [c for c in world_population.columns if c.isdigit() and int(c) >=1980]

    #keeps only the country name and selected year column
    world_population_filtered = world_population_filtered[["Country Name"] + year_cols]
    return world_population_filtered

def convert_to_long(world_population_filtered):
    #converts from wide format to long format as original dataset contains multiple columns
    year_cols = [c for c in world_population_filtered.columns if c.isdigit()]
    world_population_long = world_population_filtered.melt(
        id_vars="Country Name",
        value_vars=year_cols,
        var_name="Year",
        value_name="Population"
    )
    return world_population_long

def sort_and_fix(world_population_long):
    #Sorts the data by country and year, making it easier for analysing data 
    world_population_long = world_population_long.sort_values(
        by=["Country Name", "Year"],
        ascending=[True, True]
    )

    #validates datatype in year column to ensure all data values are integers
    world_population_long["Year"] = world_population_long["Year"].astype(int)
    return world_population_long

def world_population_cleaning():
    # full pipeline using the smaller functions
    world_population = load()
    world_population_filtered = filter(world_population)
    world_population_long = convert_to_long(world_population_filtered)
    world_population_long = sort_and_fix(world_population_long)

    # saves cleaned dataset within given directory without index values
    world_population_long.to_csv(
        "World_population/new_world_population.csv",
        index=False,
    )
    print("Run Successfully")
    return world_population_long


if __name__ == "__main__":
    world_population_cleaning()