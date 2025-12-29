import pandas as pd
import matplotlib.pyplot as plt
import os

dataset=pd.read_csv("analysis_dataset.csv")
dataset["Year"]=pd.to_numeric(dataset["Year"],errors="coerce")

countries = ["World"]

subplot = []
for country in countries:
    data_country=(dataset[dataset["Country Name"]==country]
                  .sort_values("Year")
                  .copy())
    
    data_country["CO2_percentage_change"] = (
        data_country["CO2 per capita (Trillions)"].pct_change()*100
    )

    data_country["GDP_percentage_change"] = (
        data_country["GDP per capita"].pct_change()*100
    )

    subplot.append(data_country)

change=pd.concat(subplot, ignore_index=True)

fig,axes = plt.subplots(2,1,figsize=(10,8), sharex=True)

for country in countries:
    data_country = change[change["Country Name"]==country]
    axes[0].plot(data_country["Year"],data_country["CO2_percentage_change"],
                 marker="o",linewidth=1.5,color="tab:red")

axes[0].axhline(0, color ="black", linewidth=1)
axes[0].set_ylabel("% change")
axes[0].set_title("Annual % change in CO2 emissions per capita since 1980")
axes[0].grid(True, alpha=0.3)

for country in countries:
    data_country = change[change["Country Name"] ==country]
    axes[1].plot(data_country["Year"],data_country["GDP_percentage_change"],
                 marker="o",linewidth=1.5,color="tab:red")

axes[1].axhline(0,color="black",linewidth=1)
axes[1].set_xlabel("Year")
axes[1].set_ylabel("% change")
axes[1].set_title("Annual % change in GDP per capita since 1980")
axes[1].grid(True,alpha=0.3)

for ax in axes:
    ax.spines["top"].set_visible(True)
    ax.spines["right"].set_visible(True)

folder="Graphs"
os.makedirs(folder,exist_ok=True)
plt.savefig(os.path.join(folder,"co2_gdp_annual_%_change.png"))

plt.tight_layout()
plt.show()