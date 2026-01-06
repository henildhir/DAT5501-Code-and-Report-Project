#This imports all relevant functions from the libraries for the code to run properly
import pandas as pd
import matplotlib.pyplot as plt
import os

def load(filepath):
    #Reads the analysis dataset, puts it into a variable and converts the year column to numeric values
    dataset=pd.read_csv(filepath)
    dataset["Year"]=pd.to_numeric(dataset["Year"],errors="coerce")
    return dataset

def filter_and_calculate(dataset, countries):
    #Filters the countries for the given unit case and creates an empty list for both subplots
    subplot = []

    #loops through all countries in the given country list
    for country in countries:
        data_country=(dataset[dataset["Country Name"]==country]
                    .sort_values("Year")
                    .copy())
        #Calculates the annual co2 percentage change for each country
        data_country["CO2_percentage_change"] = (
            data_country["CO2 per capita (Trillions)"].pct_change()*100
        )
        #Calculates the annual gdp percentage change for each country
        data_country["GDP_percentage_change"] = (
            data_country["GDP per capita"].pct_change()*100
        )
        #allows for all countries to be added onto the subplot
        subplot.append(data_country)

    #concatenates all the subplots into a panda array
    change=pd.concat(subplot, ignore_index=True)
    return change

def create_plots(change,countries):
    #creates an array of 2 rows for both figures with a specified figure size
    fig,axes = plt.subplots(2,1,figsize=(10,9))

    #loops through each country in the countries list and plots its corresponding annual co2 percentage change
    for country in countries:
        data_country = change[change["Country Name"]==country]
        axes[0].plot(data_country["Year"],data_country["CO2_percentage_change"],
                    marker="o",linewidth=1.5,color="tab:red")

    #creates and sets the y,x and title labels and shows the grid for the first plot
    axes[0].axhline(0, color ="black", linewidth=1)
    axes[0].set_ylabel("% change",fontsize=11)
    axes[0].set_xlabel("Year",fontsize=11)
    axes[0].set_title("Annual % change of the world in CO2 emissions per capita since 1980",fontsize=11)
    axes[0].grid(True, alpha=0.3)

    #loops through each country in the countries list and plots its corresponding gdp percentage change in the second plot
    for country in countries:
        data_country = change[change["Country Name"] ==country]
        axes[1].plot(data_country["Year"],data_country["GDP_percentage_change"],
                    marker="o",linewidth=1.5,color="tab:red")

    #creates and sets the y,x and title labels and shows the grid for the second plot
    axes[1].axhline(0,color="black",linewidth=1)
    axes[1].set_xlabel("Year",fontsize=11)
    axes[1].set_ylabel("% change",fontsize=11)
    axes[1].set_title("Annual % change of the world in GDP per capita since 1980",fontsize=11)
    axes[1].grid(True,alpha=0.3)

    #loops through both axes to set all the properties and visuals
    for ax in axes:
        #makes sure that the top and right borders are shown for both axes
        ax.spines["top"].set_visible(True)
        ax.spines["right"].set_visible(True)
        #creates a grey rectange between 2008 and 2009 to show the period of the 2008 financial crisis
        ax.axvspan(2008,2009,color="grey",alpha=0.35,label="2008 financial crisis")
        y_top=ax.get_ylim()[1]
        #labels the 2008 financial crisis at the top of the rectange, increasing the readibility of the graph
        ax.text(2008.5,y_top,"2008 financial crisis",ha="center",va="top",fontsize=8,color="black")
    return fig,axes

def save_plot(fig,folder,filename):
    #makes sure that the plot is saved within the graphs folder and validates whether a folder for graphs has been createed or not
    os.makedirs(folder,exist_ok=True)
    filepath=(os.path.join(folder,filename))
    fig.savefig(filepath)

def run():
    filepath="analysis_dataset.csv"
    countries=["World"]
    folder="Annual_percentage_change"
    filename="co2_gdp_annual_percentage_change.png"

    dataset=load(filepath)
    change = filter_and_calculate(dataset,countries)
    fig, _ = create_plots(change, countries)
    save_plot(fig, folder, filename)
    #shows the plots
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run()