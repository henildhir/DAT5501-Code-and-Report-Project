#This imports all relevant functions from the libraries for the code to run properly
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import pearsonr
import statsmodels.api as sm
import numpy as np
import os

#loads the predefined filepath ready to be analysed with year column converted to numeric values to ensure consistency throughout
def load(filepath):
    dataset=pd.read_csv(filepath)
    dataset["Year"]=pd.to_numeric(dataset["Year"],errors="coerce")
    #returns dataset to be used in another function
    return dataset

#filters dataset for the last 10 years and returns filtered dataset with minimum and maximum year
def filter_10_years(dataset): 
    max_year=dataset["Year"].max()
    min_year=max_year-9
    #filtered dataset made with only having years between given max and min year
    filter=dataset[(dataset["Year"]>=min_year)&(dataset["Year"]<=max_year)]
    return filter,min_year,max_year

#selects the x and y values from the dataset by filtering for 'World' 
def select(dataset):
    world=dataset[dataset["Country Name"]=="World"].copy()
    #only values for x and y are copied to ensure consistency and no other values are copied from another column
    x=world["GDP per capita"].values
    y=world["CO2 per capita (Trillions)"].values
    return x,y

#performs regression using pearsonr with x and y values
def regression(x,y):
    r,p=pearsonr(x,y)
    X=sm.add_constant(x)
    #uses OLS model to fit both x and y for regression
    model=sm.OLS(y,X).fit()
    #creates a numpy array with 200 x values between min and max value to ensure resolution of regression line is clear
    x_grid=np.linspace(x.min(),x.max(),200)
    X_grid=sm.add_constant(x_grid)

    #generates all the statistics for upper and lower confidence bands to be used later for 95% confidence band
    prediction=model.get_prediction(X_grid)
    prediction_summary = prediction.summary_frame(alpha=0.05)
    y_hat=prediction_summary["mean"].values

    #statistoics provided show the upper and lower confidence intervals and only values are copied, 95% CI used to show where all datapoints lie
    ci_lower=prediction_summary["mean_ci_lower"].values
    ci_upper=prediction_summary["mean_ci_upper"].values
    return r,x_grid,y_hat,ci_lower,ci_upper

#creates figure and all plots, returns fig and axes
def create_plots(filter, x_world, y_world, r, x_grid, y_hat, ci_lower, ci_upper):
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

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
            "Malawi":"orange",},
        ax=axes[0],)

    #axis labels, titles and legend added to plot for better readability
    axes[0].set_xlabel("GDP per capita ($)")
    axes[0].set_ylabel("CO2 emissions per capita (tonnes)")
    axes[0].set_title("CO2 per capita vs GDP per capita (last 10 years)",fontsize=10)
    axes[0].legend(loc="best",
                fontsize=8)
    axes[0].grid(True, alpha=0.3)

    #plots a scatter graph of original dataset values with a clear label for better readability
    axes[1].scatter(x_world,
                    y_world,
                    color="red",
                    alpha=0.55,
                    label="World data")

    #generates values for function ax+b for any x values
    coeffs=np.polyfit(x_world,y_world,1)
    poly=np.poly1d(coeffs)
    #generates a numpy array with 100 x values between both min and max values to make regression line clearer
    x_line = np.linspace(x_world.min(),x_world.max(),100)

    #plots the regression line of all observed data points 
    axes[1].plot(x_line,
                poly(x_line),
                color="black",
                label="Linear fit")

    #fills blue between both CI lower and CI upper bands to emphasise the 95% confidence band
    axes[1].fill_between(
        x_grid,
        ci_lower,
        ci_upper,
        color="blue",
        alpha=0.15,
        label="95% CI")
 
    #Axis labels, titles and legend added to plot to increase readability
    axes[1].set_xlabel("GDP per capita ($)")
    axes[1].set_ylabel("CO2 emissions per capita (tonnes)")
    axes[1].set_title("World CO2 emissions per capita vs GDP per capita (linear regression)",fontsize=10)
    axes[1].grid(True, alpha=0.4)
    axes[1].legend(loc="best",
                fontsize=8)

    #text added for calculated correlation coefficient on top right of plot to increase readability and improved visualisation
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
    return fig,axes

#saves plot with desired file name within pre-defined folder
def save(fig,folder,filename):
    os.makedirs(folder, exist_ok=True)
    plt.savefig(os.path.join(folder, filename))

#main function created to run with configuration settings of filepath, filename and folder. saves plot in given folder
def run():
    filepath = "Analysis_dataset/analysis_dataset.csv"
    folder = "co2_emissions_vs_gdp_per_capita"
    filename = "co2_emissions_gdp_per_capita.png"
    dataset = load(filepath)
    filter, min_year, max_year = filter_10_years(dataset)
    x_world, y_world = select(dataset)
    #all regression statistics passed back into variables for later statistical analysis 
    r, x_grid, y_hat, ci_lower, ci_upper = regression(x_world, y_world)

    #plots the confidence interval including observed x and y values
    fig, axes = create_plots(filter, x_world, y_world, r, x_grid, y_hat, ci_lower, ci_upper)
    save(fig, folder, filename)
    #shows the plots
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run()