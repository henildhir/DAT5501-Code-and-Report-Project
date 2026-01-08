#imports relevants functions used within this file
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analysis_dataset_merging():
    #uses pandas to read all relevant csv files with given diretory
    gdp = pd.read_csv("World_gdp/new_world_gdp.csv")
    population = pd.read_csv("World_population/new_world_population.csv")
    co2 = pd.read_csv("World_co2/new_co2_emissions_per_capita.csv")

    #merges all csv files together for easier access and analysing data
    merged = gdp.merge(population, on=["Country Name","Year"], how="inner")
    merged = merged.merge(co2,on=["Country Name","Year"], how="inner")
    merged=merged.sort_values(["Country Name", "Year"])

    #drops column 'code' as column 'country name' is already included for consistency and fewer errors
    if "Code" in merged.columns:
        merged = merged.drop(columns=["Code"])

    #renamed column name for better readability and access
    merged= merged.rename(columns={"CO2 per capita":"CO2 per capita (Trillions)","Population":"Population (Millions)"})

    #divides each column to an appropriate level of accuracy for plotting data
    merged["GDP (Trillions USD($))"]=merged["GDP"]/1e12
    merged["Population (Millions)"]=merged["Population (Millions)"]/1e6
    merged["GDP per capita"] = (merged["GDP (Trillions USD($))"]*1e6 / merged["Population (Millions)"])

    #ensures that multiple columns are removed as they are irrelevant
    #if "Code" in merged.columns:
    #  merged = merged.drop(columns=["Code"])

    #if "GDP" in merged.columns:
    #  merged=merged.drop(columns=["GDP"])
        
    #if "," in merged.columns:
    #  merged=merged.drop(columns=[","])

    #drops index values within the dataset
    merged = merged.reset_index(drop=True)

    print(merged.head())
    #saves the dataset to a defined csv file excluding index values
    merged.to_csv("Analysis_dataset/analysis_dataset.csv", index="False")

if __name__ == "__main__":
    analysis_dataset_merging()