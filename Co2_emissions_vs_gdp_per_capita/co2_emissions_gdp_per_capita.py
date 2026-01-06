#This imports all relevant functions from the libraries for the code to run properly
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import pearsonr
import statsmodels.api as sm
import numpy as np
import os

def create_plots():
    #Reads dataset and validates whether folder for graph has been created
    dataset = pd.read_csv("analysis_dataset.csv")
    folder="Co2_emissions_vs_gdp_per_capita"
    os.makedirs(folder,exist_ok=True)

    #filters the dataset for minimum and maximum years and creates an array of plots
    max_year=dataset["Year"].max()
    min_year=max_year-9
    filter=dataset[(dataset["Year"]>=min_year)&(dataset["Year"]<=max_year)]
    fig,axes = plt.subplots(1,2,figsize=(10,5))

    #a scatter plot is created with given x and y values from filtered dataset, with appropriate colours
    ax = sns.scatterplot(
        data=filter,
        x="GDP per capita",
        y="CO2 per capita (Trillions)",
        hue="Country Name",
        marker="o",
        alpha=0.4,
        palette={
            "United Kingdom":"green",
            "World":"red",
            "India":"blue",
            "Malawi":"orange",
        },
        ax=axes[0],
    )

    #Axis labels, titles and legend added to plot
    axes[0].set_xlabel("GDP per capita ($)")
    axes[0].set_ylabel("CO2 emissions per capita (tonnes)")
    axes[0].set_title("CO2 per capita vs GDP per capita (last 10 years)",fontsize=10)
    axes[0].legend(loc="best",
                fontsize=8)
    axes[0].grid(True, alpha=0.3)

    #filters dataset for given country and converts appropriate x and y values from given dataset
    world=dataset[dataset["Country Name"]=="World"].copy()
    x=world["GDP per capita"].values
    y=world["CO2 per capita (Trillions)"].values

    #computes pearson correlation between gdp per capita and co2 per capita 
    r,p=pearsonr(x,y)
    X=sm.add_constant(x)
    model=sm.OLS(y,X).fit()

    #generates an array of 100 x values between max and min value
    x_grid=np.linspace(x.min(),
                    x.max(),
                    200)
    X_grid=sm.add_constant(x_grid)

    #generates all the statistics for upper and lower confidence bands to be used later for 95% confidence band
    prediction=model.get_prediction(X_grid)
    prediction_summary = prediction.summary_frame(alpha=0.05)
    y_hat=prediction_summary["mean"].values
    ci_lower=prediction_summary["mean_ci_lower"].values
    ci_upper=prediction_summary["mean_ci_upper"].values

    #plots a scatter graph of original dataset values with a clear label
    axes[1].scatter(x,
                    y,
                    color="red",
                    alpha=0.55,
                    label="World data"
                    )

    #generates values for function ax+b for any x values
    coeffs=np.polyfit(x,y,1)
    poly=np.poly1d(coeffs)
    x_line = np.linspace(x.min(),
                        x.max(),
                        100)

    #plots the regression line of all observed data points 
    axes[1].plot(x_line,
                poly(x_line),
                color="black",
                label="Linear fit"
                )

    #fills blue between both CI lower and CI upper bands to emphasise the 95% confidence band
    axes[1].fill_between(
        x_grid,
        ci_lower,
        ci_upper,
        color="blue",
        alpha=0.15,
        label="95% CI"
    )

    #Axis labels, titles and legend added to plot
    axes[1].set_xlabel("GDP per capita ($)")
    axes[1].set_ylabel("CO2 emissions per capita (tonnes)")
    axes[1].set_title("World CO2 emissions per capita vs GDP per capita (linear regression)",fontsize=10)
    axes[1].grid(True, alpha=0.4)
    axes[1].legend(loc="best",
                fontsize=8)

    #text added for calculated correlation coefficient on top right of plot
    axes[1].text(0.05,
                0.95,
                f"r={r:.2f}",
                transform=axes[1].transAxes,
                ha="left",
                va="top")

    #ensures all axes have borders around, making graphs look clean
    for ax in axes:
        ax.spines["top"].set_visible(True)
        ax.spines["right"].set_visible(True)

    #saves plot with desired file name within pre-defined folder
    plt.savefig(os.path.join(folder,"co2_emissions_gdp_per_capita.png"))
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    create_plots()