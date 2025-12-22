import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

gdp = pd.read_csv("World_gdp/new_world_gdp.csv")
population = pd.read_csv("World_population/new_world_population.csv")
co2 = pd.read_csv("World_co2/new_co2_emissions_per_capita.csv")

merged = gdp.merge(population, on=["Country Name","Year"], how="inner")
merged = merged.merge(co2,on=["Country Name","Year"], how="inner")
merged=merged.sort_values(["Country Name", "Year"])

if "Code" in merged.columns:
    merged = merged.drop(columns=["Code"])

merged= merged.rename(columns={"CO2 per capita":"CO2 per capita (Trillions)","Population":"Population (Millions)"})

merged["GDP (Trillions USD($))"]=merged["GDP"]/1e12
merged["Population (Millions)"]=merged["Population (Millions)"]/1e6
merged["GDP per capita (Thousand USD ($))"] = (merged["GDP (Trillions USD($))"]*1e6 / merged["Population (Millions)"])

# if "Code" in merged.columns:
#     merged = merged.drop(columns=["Code"])

# if "GDP" in merged.columns:
#     merged=merged.drop(columns=["GDP"])
    
# if "," in merged.columns:
#     merged=merged.drop(columns=[","])

merged = merged.reset_index(drop=True)

print(merged.head())
print(merged.columns)

merged.to_csv("analysis_dataset.csv", index="False")

dataset = pd.read_csv("analysis_dataset.csv")

plt.figure(figsize=(10,6))
sns.lineplot(data=dataset,x="Year",
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

plt.axvline(x=Paris_agreement,color="grey",linestyle="--",linewidth=1.5,alpha=0.7,label=f"{Paris_agreement} Paris Agreement")
handles,labels = plt.gca().get_legend_handles_labels()
plt.legend(handles,labels,title="Country/Event",loc="best")

plt.tight_layout()
plt.show()
