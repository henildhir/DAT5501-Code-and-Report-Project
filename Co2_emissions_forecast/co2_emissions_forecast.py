import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_dataset(filepath):
    """Reads the dataset and converts Year column to numeric values."""
    dataset = pd.read_csv(filepath)
    dataset["Year"] = pd.to_numeric(dataset["Year"], errors="coerce")
    return dataset

def get_config():
    countries = ["United Kingdom", "World", "India", "Malawi"]
    colors = {
        "United Kingdom": "green",
        "World": "red",
        "India": "blue",
        "Malawi": "orange",
    }

    degrees = {
        "United Kingdom": 2,
        "India": 2,
        "World": 1,
        "Malawi": 1,
    }
    return countries, colors, degrees

def prepare_country_data(dataset, country):
    country_data = (
        dataset[dataset["Country Name"] == country]
        .sort_values("Year")
    )
    x_train = country_data["Year"].values
    y_train = country_data["CO2 per capita (Trillions)"].values
    return country_data, x_train, y_train

def fit_and_forecast(x_train, y_train, degree):
    max_year = x_train.max()
    coeffs = np.polyfit(x_train, y_train, degree)
    poly = np.poly1d(coeffs)

    x_forecast = np.arange(x_train.min(), max_year + 10)
    y_forecast = poly(x_forecast)

    historical = x_forecast <= max_year
    future = x_forecast >= max_year
    return x_forecast, y_forecast, historical, future

def plot_country_forecast(country, colors, x_train, y_train,x_forecast, y_forecast, historical, future):
    plt.plot(
        x_forecast[historical],
        y_forecast[historical],
        color=colors[country],
        linewidth=1.5,
    )
    # future forecast
    plt.plot(
        x_forecast[future],
        y_forecast[future],
        color=colors[country],
        linestyle="--",
        linewidth=2.5,
        label=f"{country} forecasting",
    )
    # actual points
    plt.scatter(
        x_train,
        y_train,
        color=colors[country],
        label=f"{country} data",
        zorder=5,
        s=25,
    )

def setup_figure():
    """Sets up figure size."""
    plt.figure(figsize=(10, 6))

def finalize_plot():
    plt.xlabel("Year")
    plt.ylabel("CO2 emissions per capita (tonnes)")
    plt.title("CO2 emissions forecasting for the next 10 years")

    plt.axvline(
        x=2024,
        color="grey",
        linestyle="--",
        linewidth=1.5,
        alpha=0.7,
    )
    plt.ylim(-0.2, None)
    plt.grid(True, alpha=0.4)
    plt.legend(loc="best", fontsize="small")

    folder = "Co2_emissions_forecast"
    os.makedirs(folder, exist_ok=True)
    plt.savefig(os.path.join(folder, "co2_emissions_forecasting.png"))
    plt.tight_layout()
    plt.show()

def co2_emissions_forecast(filepath):
    dataset = load_dataset(filepath)
    countries, colors, degrees = get_config()
    setup_figure()
    results = {}
    for country in countries:
        country_data, x_train, y_train = prepare_country_data(dataset, country)
        x_forecast, y_forecast, historical, future = fit_and_forecast(
            x_train, y_train, degrees[country]
        )

        plot_country_forecast(
            country,
            colors,
            x_train,
            y_train,
            x_forecast,
            y_forecast,
            historical,
            future,
        )

        results[country] = (
            country_data,
            x_train,
            y_train,
            x_forecast,
            y_forecast,
            historical,
            future,
        )

    finalize_plot()
    return dataset, results

def run():
    filepath = "analysis_dataset.csv"
    co2_emissions_forecast(filepath)

if __name__ == "__main__":
    run()