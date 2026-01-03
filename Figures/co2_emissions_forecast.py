import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

dataset = pd.read_csv("analysis_dataset.csv")
dataset["Year"] = pd.to_numeric(dataset["Year"],errors="coerce")

countries = ["United Kingdom","World","India","Malawi"]
colors = {"United Kingdom":"green",
          "World":"red",
          "India":"blue",
          "Malawi":"orange"}

degrees = {"United Kingdom":2,
           "India":2,
           "World":1,
           "Malawi":1}

plt.figure(figsize=(10,6))
lines=[]

for country in countries:
    country_data = (dataset[dataset["Country Name"] == country].sort_values("Year"))

    x_train = country_data["Year"].values
    y_train = country_data["CO2 per capita (Trillions)"].values

    max_year=x_train.max()
    deg = degrees[country]

    coeffs = np.polyfit(x_train,y_train,deg)
    poly = np.poly1d(coeffs)

    x_forecast = np.arange(x_train.min(),max_year + 10)
    y_forecast = poly(x_forecast)

    historical = x_forecast <= max_year
    future = x_forecast >= max_year

    plt.plot(
        x_forecast[historical],
        y_forecast[historical],
        color=colors[country],
        linewidth=1.5,
    )          
    
    plt.plot(x_forecast[future],
                y_forecast[future],
                color=colors[country],
                linestyle="--",
                linewidth=2.5,
                label=f"{country} forecasting")

    plt.scatter(x_train,
                y_train,
                color=colors[country],
                label =f"{country} data",
                zorder=5,
                s=25)

plt.xlabel("Year")
plt.ylabel("CO2 emissions per capita (tonnes)")
plt.title("CO2 emissions forecasting for the next 10 years")
plt.axvline(x=2024,color="grey",linestyle="-",linewidth=1.5,alpha=0.7)
plt.ylim(-0.2,None)
plt.grid(True,alpha=0.4)

# plt.legend(handles=lines + [plt.Line2D([], [], marker="o", color=colors[country],linestyle="",label=f"{country} data")], loc="best")
plt.legend(loc="best",fontsize="small")

folder="Graphs"
os.makedirs(folder,exist_ok=True)
plt.savefig(os.path.join(folder,"co2_emissions_forecasting.png"))
plt.tight_layout()
plt.show()