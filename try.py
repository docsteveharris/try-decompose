import sys

import polars as pl
from matplotlib import pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# fetch dataset (133MB so this command takes ages)
# individual_household_electric_power_consumption = fetch_ucirepo(id=235)
# X = individual_household_electric_power_consumption.data.features


# Import just power, rename, specify data types, and deal with missing values
X = pl.read_csv(
    "./household_power_consumption.txt",
    columns=["Date", "Time", "Global_active_power"],
    new_columns=["date", "time", "power"],
    schema=pl.Schema(
        {"Date": pl.Date, "Time": pl.Time, "Global_active_power": pl.Float32}
    ),
    truncate_ragged_lines=True,
    separator=";",
    has_header=True,
    null_values=["?"],
)

# Combine date and time columns into a datetime column
X = X.with_columns(
    [
        pl.col("date").dt.combine(pl.col("time")).alias("datetime"),
    ]
)
X = X.drop(["date", "time"])
X = X.select(["datetime", "power"])


# Plot the time series graph
plt.figure(figsize=(12, 4))
plt.plot(X["datetime"], X["power"])
plt.title("Global Active Power Over Time")
plt.xlabel("Date")
plt.ylabel("Global Active Power")
plt.grid(True)
plt.show()

# Seasonal decomposition fails with missing values
# Count missing rows
missing_rows = X["power"].is_null().sum()
print(f"Number of missing rows: {missing_rows}")
# So fill missing values with the previous non-missing value
X = X.fill_null(strategy="forward")
# Quick slice of the data to test seasonal decomposition
X1 = X.head(2 * 60 * 24 * 7)

X1 = X1.to_pandas()
X1.set_index("datetime")
# remove the weekly seasonality
weekly_decomposition = seasonal_decompose(
    X1,
    model="additive",
    period=60 * 24 * 7,
    two_sided=False,
)
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

print("Success")
sys.exit()
