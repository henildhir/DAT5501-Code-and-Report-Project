import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import pearsonr
import statsmodels.api as sm
import numpy as np
import os

dataset = pd.read_csv("analysis_dataset.csv")
folder="Graphs"
os.makedirs(folder,exist_ok=True)

max_year=dataset["Year"].max()
min_year=max_year-9
filter=dataset[(dataset["Year"]>=min_year)&(dataset["Year"]<=max_year)]

fig,axes = plt.subplots(1,2,figsize=(10,5))

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

axes[0].set_xlabel("GDP per capita ($)")
axes[0].set_ylabel("CO2 emissions per capita (tonnes)")
axes[0].set_title("CO2 per capita vs GDP per capita (last 10 years)",fontsize=10)
axes[0].legend(loc="best",
               fontsize=8)
axes[0].grid(True, alpha=0.3)

world=dataset[dataset["Country Name"]=="World"].copy()
x=world["GDP per capita"].values
y=world["CO2 per capita (Trillions)"].values

r,p=pearsonr(x,y)

X=sm.add_constant(x)
model=sm.OLS(y,X).fit()

x_grid=np.linspace(x.min(),
                   x.max(),
                   200)
X_grid=sm.add_constant(x_grid)

prediction=model.get_prediction(X_grid)
prediction_summary = prediction.summary_frame(alpha=0.05)
y_hat=prediction_summary["mean"].values
ci_lower=prediction_summary["mean_ci_lower"].values
ci_upper=prediction_summary["mean_ci_upper"].values

axes[1].scatter(x,
                y,
                color="red",
                alpha=0.55,
                label="World data"
                )

coeffs=np.polyfit(x,y,1)
poly=np.poly1d(coeffs)
x_line = np.linspace(x.min(),
                     x.max(),
                     100)

axes[1].plot(x_line,
             poly(x_line),
             color="black",
             label="Linear fit"
             )
axes[1].fill_between(
    x_grid,
    ci_lower,
    ci_upper,
    color="blue",
    alpha=0.15,
    label="95% CI"
)
axes[1].set_xlabel("GDP per capita ($)")
axes[1].set_ylabel("CO2 emissions per capita (tonnes)")
axes[1].set_title("World CO2 emissions per capita vs GDP per capita (linear regression)",fontsize=10)
axes[1].grid(True, alpha=0.4)
axes[1].legend(loc="best",
               fontsize=8)

axes[1].text(0.05,
             0.95,
             f"r={r:.2f}",
             transform=axes[1].transAxes,
             ha="left",
             va="top")

for ax in axes:
    ax.spines["top"].set_visible(True)
    ax.spines["right"].set_visible(True)

plt.savefig(os.path.join(folder,"co2_emissions_gdp_per_capita.png"))
plt.tight_layout()
plt.show()