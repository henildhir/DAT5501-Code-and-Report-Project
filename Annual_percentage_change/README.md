# CO2 Emissions per Capita and GDP per Capita – Annual Percentage Change Analysis

This folder analyses how **World CO2 emissions per capita** and **World GDP per capita** have changed annually since 1980, with a particular focus on the **2008 financial crisis**. The analysis is part of a broader business problem: understanding how global economic shocks affect emissions, which is relevant for firms and investors exposed to carbon‑intensive activities and transition risk.

The main script described here is `annual_%_change.py`. It produces a figure with two time‑series plots:

1. Annual % change in world CO2 emissions per capita  
2. Annual % change in world GDP per capita  

A grey shaded band highlights the period 2008–2009 to show the impact of the financial crisis on both series.

---

## Features

- Loads data from `analysis_dataset.csv`
- Filters data for a specified list of countries (default: `["World"]`)
- Calculates:
  - Annual % change in **CO₂ per capita (Trillions)**  
  - Annual % change in **GDP per capita**
- Produces a figure with 2 subplots:
  1. Annual % change in CO₂ emissions per capita since 1980  
  2. Annual % change in GDP per capita since 1980
- Highlights the **2008–2009 financial crisis** period with a shaded region and label
- Saves the figure as `co2_gdp_annual_%_change.png` inside the `Annual_%_change/` folder

---

## Customisation Notes 

The dataset provided in `analysis_dataset.csv` has data values from only 4 unit cases: **United Kingdom, World, India and Malawi**. This is due to the varying economic levels each unit case has. For example the UK is a developed country with an **extremely high GDP per capita** relative to Malawi thus allowing for comparisons to be made regarding co2 emissions. 

In this case, the unit case of the entire world has been chosen to show the annual percentage change in GDP per capita and CO2 emissions per capita. This unit case can be changed to simulate other nations worldwide, showing the different gdp per capita levels compared to co2 emissions per capita.

---

## Design Decisions and Performance Justifications

### Vectorised calculations with pandas:
- Annual % changes are computed using `data_country["CO2 per capita (Trillions)"].pct_change()*100` and `data_country["GDP per capita"].pct_change()*100` on whole columns instead of manual Python loops. This uses fast, C‑optimised operations and scales better if more years or countries are added.

### Per‑country filtering + single concatenation:
- Each country is filtered once from the full dataset, processed, then all results are combined with a single pd.concat. This avoids repeated expensive concatenations inside the loop and keeps memory use and runtime low.

### Single figure with shared subplots:
- `fig,axes = plt.subplots(2,1,figsize=(10,9))` creates both graphs in one figure. Re‑using the same axes objects is more efficient than generating multiple figures and keeps drawing overhead small even when more countries are plotted.

### Minimal I/O:
- The CSV is read once and the plot is written to disk once. All other work is done in memory, which is faster than repeatedly accessing the file system.

---

## Interpretive Insight

The graph shows that around the **2008 financial crisis** there is a noticeable drop in both GDP per capita and CO2 emissions per capita. This suggests that major economic shocks can temporarily reduce emissions because industrial activity, transport, and energy demand all contract when GDP falls.

This is useful because it links the performance of the economy to environmental pressure: when markets crash and firms cut production and logistics, emissions decline, but for negative reasons (recession) rather than through planned decarbonisation. The graph therefore helps distinguish between emissions reductions driven by economic downturns and those driven by deliberate climate policy.

---

## Requirements

- latest python version
- Libraries:
  - `pandas`
  - `matplotlib`
  - `os` 