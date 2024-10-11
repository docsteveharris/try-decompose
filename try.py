#!/Users/steve/miniconda3/bin/python
# working with the base install of conda

import pandas as pd
from matplotlib import pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# fetch dataset (133MB so this command takes ages)
# individual_household_electric_power_consumption = fetch_ucirepo(id=235)
# X = individual_household_electric_power_consumption.data.features

# so downloaded my own copy
X = pd.read_csv(
    "household_power_consumption.txt",
    sep=";",
    header=0,
    usecols=["Date", "Time", "Global_active_power"],
    # nrows=1000,
    dtype={"Date": str, "Time": str, "Global_active_power": float},
    na_values=["?"],
)
# Fix the date and time columns, and convert to index
X["Date"] = pd.to_datetime(X["Date"], format="%d/%m/%Y")
X["Time"] = pd.to_timedelta(X["Time"])
X["DateTime"] = X["Date"] + X["Time"]
X.set_index("DateTime", inplace=True)
X.drop(columns=["Date", "Time"], inplace=True)

# Plot the time series graph
plt.figure(figsize=(12, 4))
plt.plot(X.index, X["Global_active_power"])
plt.title("Global Active Power Over Time")
plt.xlabel("Date")
plt.ylabel("Global Active Power")
plt.grid(True)
plt.show()

# Seasonal decomposition fails with missing values
# Count missing rows
missing_rows = X["Global_active_power"].isna().sum()
print(f"Number of missing rows: {missing_rows}")
# So fill missing values with the previous non-missing value
X.ffill(inplace=True)
X.head()
# Quick slice of the data to test seasonal decomposition
X1 = X.head(2 * 60 * 24 * 7)

# remove the weekly seasonality
weekly_decomposition = seasonal_decompose(X1, model="additive", period=60 * 24 * 7)
weekly_trend = weekly_decomposition.trend
weekly_decomposition.plot()

# remove the daily seasonality
daily_decomposition = seasonal_decompose(
    weekly_trend.dropna(), model="additive", period=60 * 24
)
daily_trend = daily_decomposition.trend
daily_decomposition.plot()

# remove the hourly seasonality
hourly_decomposition = seasonal_decompose(
    daily_trend.dropna(), model="additive", period=60
)
hourly_decomposition.plot()


# Final compooneents
raw = X1["Global_active_power"]
trend = hourly_decomposition.trend
hourly_seasonal = hourly_decomposition.seasonal
daily_seasonal = daily_decomposition.seasonal
weekly_seasonal = weekly_decomposition.seasonal

residual = raw - trend - hourly_seasonal - daily_seasonal - weekly_seasonal
residual.plot()
