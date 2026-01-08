#This imports all relevant functions from the libraries for the code to run properly
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

#loads the predefined filepath ready to be analysed with year column converted to numeric values to ensure consistency throughout
def load(filepath):
    dataset=pd.read_csv(filepath)
    dataset["Year"]=pd.to_numeric(dataset["Year"],errors="coerce")
    return dataset

def key_figure_creation(dataset):
        #plot given appropriate figure size and a lineplot is created using seaborn which given attributes and x and y values
        #plot shows co2 per capita over time for each country
        plt.figure(figsize=(10,6))
        ax = sns.lineplot(data=dataset,x="Year",
                y="CO2 per capita (Trillions)",
                hue="Country Name",
                marker="o",
                linewidth=2,
                markersize=5)

        #axis labels, titles and legend added to plot to improve readability
        plt.xlabel=("Year")
        plt.ylabel("Co2 emissions per capita (tonnes)")
        plt.title("CO2 emissions per capita (tonnes) over time since 1980")
        plt.grid(True,alpha=0.3)

        #vertical line created at 2015 to show historical events as a dashed line to improve readability 
        Paris_agreement=2015
        plt.axvline(x=Paris_agreement,color="grey",linestyle="--",linewidth=1.5,alpha=0.7,label="2015 Paris Agreement")

        #reorder legend entries to match narrative order in the report to improve readability, easier to distinguish which lines belong to which country
        order=["United Kingdom",
                "World",
                "India",
                "Malawi",
                "2015 Paris Agreement"]

        #creates handles and labels for the legend for the corresponding country in order
        handles,labels = ax.get_legend_handles_labels()
        new_handles=[]
        new_labels=[]
        #loops through all countries and attaches its corresponding label to improve readability
        for country in order:
                if country in labels:
                        idx=labels.index(country)
                        new_handles.append(handles[idx])
                        new_labels.append(labels[idx])

        #plots the legend to ensure consistency throughout
        plt.legend(handles=new_handles,labels=new_labels,title="Country/Event",loc="best")
        plt.tight_layout()
        fig=plt.gcf()
        return fig,ax

#validates whether that folder has been created before, if not it will create one
def save_figure(fig, folder, filename):
        os.makedirs(folder,exist_ok=True)
        fig.savefig(os.path.join(folder,filename))

#main function created to run with configuration settings of filepath, filename and folder. saves plot in given folder
def run():
    filepath="Analysis_dataset/analysis_dataset.csv"
    folder="Key_figure"
    filename="key_figure.png"

    dataset = load(filepath)
    fig, _ = key_figure_creation(dataset)
    save_figure(fig, folder, filename)
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    run()
