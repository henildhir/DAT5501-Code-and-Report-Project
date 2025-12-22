import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

dataset = pd.read_csv("analysis_dataset.csv")

plt.figure(figsize=(10,6))
ax = sns.lineplot(data=dataset,x="Year",
             y="CO2 per capita (Trillions)",
             hue="Country Name",
             marker="o",
             linewidth=2,
             markersize=5)
plt.xlabel=("Year")
plt.ylabel("Co2 emissions per capita (tonnes)")
plt.title("CO2 emissions per capita (tonnes) over time since 1980")
plt.grid(True,alpha=0.3)

Paris_agreement=2015

plt.axvline(x=Paris_agreement,color="grey",linestyle="--",linewidth=1.5,alpha=0.7,label="2015 Paris Agreement")

order=["United Kingdom","World","India","Malawi","2015 Paris Agreement"]
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

folder="Graphs"
os.makedirs(folder,exist_ok=True)
plt.savefig(os.path.join(folder,"co2_emissions_per_capita.png"))
plt.show()