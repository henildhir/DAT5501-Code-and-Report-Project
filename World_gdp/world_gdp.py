#imports relevants functions used within this file
import pandas as pd

def load():
    #uses pandas to read csv file and skips first 4 rows as they do not contain any data
    world_gdp = pd.read_csv("World_gdp/world_gdp.csv", skiprows=4)
    return world_gdp

def filter(world_gdp):
    #filters out the desired countries given within the countries list
    countries =["United Kingdom","India","Malawi","World"]
    world_gdp_filtered=world_gdp[world_gdp["Country Name"].isin(countries)]

    #only selectes the year column and filters for values that are 1980 or after
    year_cols = [c for c in world_gdp_filtered.columns if c.isdigit() and int(c) >= 1980]
    world_gdp_filtered=world_gdp_filtered[["Country Name"]+year_cols]
    return world_gdp_filtered

#converts from wide format to long format as original dataset contains multiple columns
def convert_to_long(world_gdp_filtered):
    year_cols = [c for c in world_gdp_filtered.columns if c.isdigit()]
    world_gdp_long = world_gdp_filtered.melt(
        id_vars="Country Name",
        value_vars=year_cols,
        var_name="Year",
        value_name="GDP")
    return world_gdp_long

def sort_and_fix(world_gdp_long):
    #sorts values by country name and year in ascending order, easier for analysing data 
    world_gdp_long = world_gdp_long.sort_values(
        by=["Country Name", "Year"],
        ascending=[True, True])

    #validates datatype in year column to ensure all data values are integers
    world_gdp_long["Year"] = world_gdp_long["Year"].astype(int)
    return world_gdp_long

#cleans entire data set into long format including convert strings to numeric values
def world_gdp_cleaning():
    world_gdp = load()
    #dataset given is then filtered, converted and sorted to find any bugs or errors 
    world_gdp_filtered = filter(world_gdp)
    world_gdp_long = convert_to_long(world_gdp_filtered)
    world_gdp_long = sort_and_fix(world_gdp_long)
    #saves cleaned dataset within given directory without index values
    #this avoids saving the 0,1,2 index column
    world_gdp_long.to_csv(
        "World_gdp/new_world_gdp.csv",)
    print(world_gdp_long.head())

if __name__ == "__main__":
    world_gdp_cleaning()