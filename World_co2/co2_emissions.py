#imports relevants functions used within this file
import pandas as pd
import os

#loads the predefined filepath ready to be analysed
def load(filepath):
    #Reads the analysis dataset, puts it into a variable and converts the year column to numeric values to ensure consistency throughout
    dataset=pd.read_csv(filepath)
    dataset["Year"]=pd.to_numeric(dataset["Year"],errors="coerce")
    return dataset

def co2_emissions_cleaning(dataset):

    #filters data in year column for years 1980 and later, easier to analyse data
    co2_emissions=dataset[dataset["Year"] >= 1980]

    #renamed columns to better names, making analysing data easier and for column headers that are confusing
    co2_emissions=co2_emissions.rename(
        columns = {
            "Entity":"Country Name",
            "Annual CO₂ emissions (per capita)":"CO2 per capita",})
    return co2_emissions

#validates whether that folder has been created before, if not it will create one
def save_figure(folder, filename):
        os.makedirs(folder,exist_ok=True)
        co2_emissions=os.path.join(folder,filename)

#main function created to run with configuration settings of filepath, filename and folder. saves plot in given folder
def run():
    filepath="World_co2/co2-emissions-per-capita.csv"
    folder="World_co2"
    filename="new_co2_emissions_per_capita.png"
    dataset = load(filepath)
    #all relevant functions are run with an argument provided
    co2_emissions_cleaning(dataset)
    save_figure(folder,filename)
    #confirms whether code has run successfully to avoid confusion
    print("run successfully")
    
if __name__ == "__main__":
    run()
