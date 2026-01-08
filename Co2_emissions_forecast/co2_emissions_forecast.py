#imports all functions
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

#loads predefined dataset into function
def load_dataset(filepath):
    #Reads the dataset and converts Year column to numeric values
    dataset = pd.read_csv(filepath)
    dataset["Year"] = pd.to_numeric(dataset["Year"], errors="coerce")
    return dataset

#pre defined configuration for countries, colours and degrees
def get_config():
    countries = ["United Kingdom", "World", "India", "Malawi"]
    colors = {
        "United Kingdom": "green",
        "World": "red",
        "India": "blue",
        "Malawi": "orange",}

    #predefined dictionary for degrees for all countries when creating polynomial graphs
    degrees = {
        "United Kingdom": 2,
        "India": 2,
        "World": 1,
        "Malawi": 1,}
    return countries, colors, degrees

#filters dataset for given country and sorts by year
def prepare_country_data(dataset, country):
    country_data = (
        dataset[dataset["Country Name"] == country]
        .sort_values("Year"))
    #extracts x and y values to be used for polynomial fitting
    x_train = country_data["Year"].values
    y_train = country_data["CO2 per capita (Trillions)"].values
    return country_data, x_train, y_train

#fits a polynomial of given degree to historical CO2 data
def fit_and_forecast(x_train, y_train, degree):
    max_year = x_train.max()
    coeffs = np.polyfit(x_train, y_train, degree)
    poly = np.poly1d(coeffs)

    #creates forecast years from first observed year up to 10 years beyond last
    x_forecast = np.arange(x_train.min(), max_year + 10)
    y_forecast = poly(x_forecast)

    #splits forecast into historical period and future period
    historical = x_forecast <= max_year
    future = x_forecast >= max_year
    return x_forecast, y_forecast, historical, future

#plots all countries and its respective x and y forecast including historical and future points
def plot_country_forecast(country, colors, x_train, y_train,x_forecast, y_forecast, historical, future):
    plt.plot(
        x_forecast[historical],
        y_forecast[historical],
        color=colors[country],
        linewidth=1.5,)
    #plots future forecast using dashed line for visual distinction
    plt.plot(
        x_forecast[future],
        y_forecast[future],
        color=colors[country],
        linestyle="--",
        linewidth=2.5,
        label=f"{country} forecasting",)
    #plots original data points on top of the lines
    plt.scatter(
        x_train,
        y_train,
        color=colors[country],
        label=f"{country} data",
        zorder=5,
        s=25,)

#Sets up figure size for better visualation
def setup_figure():
    plt.figure(figsize=(10, 6))

#creates all plots and adds their axis, legend and saves file to given folder
def finalise_plot():
    plt.xlabel("Year")
    plt.ylabel("CO2 emissions per capita (tonnes)")
    plt.title("CO2 emissions forecasting for the next 10 years")

    #adds vertical line at 2024 to mark start of forecast period 
    plt.axvline(
        x=2024,
        color="grey",
        linestyle="--",
        linewidth=1.5,
        alpha=0.7,)
    #y axis limited to -0.2 so that the forecasting for the UK can be seen to reach 0
    plt.ylim(-0.2, None)
    plt.grid(True, alpha=0.4)
    plt.legend(loc="best", fontsize="small")

    #creates folder and saves the figure with a fixed file name
    folder = "Co2_emissions_forecast"
    os.makedirs(folder, exist_ok=True)
    plt.savefig(os.path.join(folder, "co2_emissions_forecasting.png"))
    plt.tight_layout()
    plt.show()

#main function for loading data, runs forecast and plots data points for each country
def co2_emissions_forecast(filepath):
    dataset = load_dataset(filepath)
    countries, colors, degrees = get_config()
    setup_figure()
    results = {}
    
    #loops through all countries for plotting observed data points
    for country in countries:
        country_data, x_train, y_train = prepare_country_data(dataset, country)
        x_forecast, y_forecast, historical, future = fit_and_forecast(x_train, y_train, degrees[country])

        #adds lines and points to the shared figure for both historical and future points with distinct colours
        plot_country_forecast(
            country,
            colors,
            x_train,
            y_train,
            x_forecast,
            y_forecast,
            historical,
            future,)

        #stores results for potential further analysis or testing, includes all data points for each country
        results[country] = (
            country_data,
            x_train,
            y_train,
            x_forecast,
            y_forecast,
            historical,
            future,)
    #runs the function and adds all necessary visuals for graph including axes labels and grid for better readability
    finalise_plot()
    return dataset, results

#runs the main function and called the combined dataset
def run():
    filepath = "Analysis_dataset/analysis_dataset.csv"
    co2_emissions_forecast(filepath)

if __name__ == "__main__":
    run()