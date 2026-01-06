#This imports all relevant functions from the libraries for the code to run properly
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def co2_emissions_forecast(filepath):
    #Reads the dataset and converts year column to numeric values to be used later for plotting
    dataset = pd.read_csv(filepath)
    dataset["Year"] = pd.to_numeric(dataset["Year"],errors="coerce")

    #Lists contain the desired countries from the dataset alongside colours to be later used for plotting, ensures readability is accurate and clear
    countries = ["United Kingdom","World","India","Malawi"]
    colors = {"United Kingdom":"green",
            "World":"red",
            "India":"blue",
            "Malawi":"orange"}

    #appropriate levels of degree used for each country for forecasting co2 emissions per capita
    degrees = {"United Kingdom":2,
            "India":2,
            "World":1,
            "Malawi":1}

    #appropriate figure size chosen for maximum retention and ensures graphs are not clustered together
    plt.figure(figsize=(10,6))
    lines=[]
    results={}
    #loops through all the countries and calculates and plots the historical and future values for co2 emissions
    for country in countries:
        country_data = (dataset[dataset["Country Name"] == country].sort_values("Year"))
        
        #selects training data for current country within the loop
        x_train = country_data["Year"].values
        y_train = country_data["CO2 per capita (Trillions)"].values
        max_year=x_train.max()
        deg = degrees[country]

        #using numpy arrays, fits a polynomial trend to historical co2 data
        coeffs = np.polyfit(x_train,y_train,deg)
        poly = np.poly1d(coeffs)

        #generates fitted values for both x and y from current year till next decade
        x_forecast = np.arange(x_train.min(),max_year + 10)
        y_forecast = poly(x_forecast)

        #splits the polynomial trend into historical and future, ensuring readability is clear throughout 
        historical = x_forecast <= max_year
        future = x_forecast >= max_year

        #plots only the historical data with appropriate colours from pre-defined list - target audience can see the colours clearly
        plt.plot(
            x_forecast[historical],
            y_forecast[historical],
            color=colors[country],
            linewidth=1.5,
        )          
        
        #plots predicted forecast of co2 emissions with different linestyle and width for next 10 years
        plt.plot(x_forecast[future],
                    y_forecast[future],
                    color=colors[country],
                    linestyle="--",
                    linewidth=2.5,
                    label=f"{country} forecasting")

        #actual data points observed with appropriate colours from pre-defined list
        plt.scatter(x_train,
                    y_train,
                    color=colors[country],
                    label =f"{country} data",
                    zorder=5,
                    s=25)
            
        results[country]=(country_data, x_train, y_train, x_forecast, y_forecast, historical, future)

    #Axis, labels, titles and legend added to plot
    plt.xlabel("Year")
    plt.ylabel("CO2 emissions per capita (tonnes)")
    plt.title("CO2 emissions forecasting for the next 10 years")
    #vertical dashed line at selected x value to reference when forecast starts for next decade
    plt.axvline(x=2024,color="grey",linestyle="-",linewidth=1.5,alpha=0.7)
    plt.ylim(-0.2,None)
    plt.grid(True,alpha=0.4)
    plt.legend(loc="best",fontsize="small")

    #Validates whether folder for graph has been created and saves plot with desired file name within folder
    folder="Co2_emissions_forecast"
    os.makedirs(folder,exist_ok=True)
    plt.savefig(os.path.join(folder,"co2_emissions_forecasting.png"))
    plt.tight_layout()
    plt.show()

    return dataset,results

def run():
    filepath = "../analysis_dataset.csv"
    co2_emissions_forecast(filepath)

if __name__ == "__main__":
    run()