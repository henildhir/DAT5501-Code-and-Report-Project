import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os

dataset = pd.read_csv("analysis_dataset.csv")

max_year=dataset["Year"].max()
min_year=max_year-9
filter=dataset[(dataset["Year"]>=min_year)&(dataset["Year"]<=max_year)]

plt.figure(figsize=(10,6))

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
)

plt.xlabel("Gdp per capita ($))")
plt.ylabel("CO2 emissions per capita (tonnes)")
plt.title("CO2 per capita vs GDP per capita")
plt.legend(title="Country",loc="lower right")

folder="Graphs"
os.makedirs(folder,exist_ok=True)
plt.savefig(os.path.join(folder,"co2_emissions_gdp_per_capita.png"))

ax.spines["top"].set_visible(True)
ax.spines["right"].set_visible(True)
ax.grid(True,alpha=0.3)
plt.savefig(os.path.join(folder,"co2_emissions_gdp_per_capita.png"))
plt.tight_layout()
plt.show()