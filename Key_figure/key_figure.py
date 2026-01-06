#This imports all relevant functions from the libraries for the code to run properly
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load(filepath):
    #Reads the analysis dataset, puts it into a variable and converts the year column to numeric values
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

        #Axis labels, titles and legend added to plot
        plt.xlabel=("Year")
        plt.ylabel("Co2 emissions per capita (tonnes)")
        plt.title("CO2 emissions per capita (tonnes) over time since 1980")
        plt.grid(True,alpha=0.3)

        #Vertical line created at 2015 to show historical events as a dashed line
        Paris_agreement=2015
        plt.axvline(x=Paris_agreement,color="grey",linestyle="--",linewidth=1.5,alpha=0.7,label="2015 Paris Agreement")

        #reorder legend entries to match narrative order in the report
        order=["United Kingdom",
                "World",
                "India",
                "Malawi",
                "2015 Paris Agreement"]

        #creates handles and labels for the legend for the corresponding country in order
        handles,labels = ax.get_legend_handles_labels()
        new_handles=[]
        new_labels=[]
        for country in order:
                if country in labels:
                        idx=labels.index(country)
                        new_handles.append(handles[idx])
                        new_labels.append(labels[idx])

        plt.legend(handles=new_handles,labels=new_labels,title="Country/Event",loc="best")
        plt.tight_layout()
        fig=plt.gcf()
        return fig,ax

def save_figure(fig, folder, filename):
        #validates whether that folder has been created before, if not it will create one
        os.makedirs(folder,exist_ok=True)
        fig.savefig(os.path.join(folder,filename))
        

def run():
    filepath="analysis_dataset.csv"
    folder="Key_figure"
    filename="key_figure.png"

    dataset = load(filepath)
    fig, _ = key_figure_creation(dataset)
    save_figure(fig, folder, filename)

    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    run()
