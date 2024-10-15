import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose

from clean_data import clean_data, fill_missing_values, filter_timeseries
from eda import plot_timeseries
from load_data import get_data_from_uci

DATA_PATH = "./data/household_power_consumption.txt"
START_DATE = "2008-01-01"
END_DATE = "2008-01-21"
WEEK_PERIOD = 60 * 24 * 7
DAY_PERIOD = 60 * 24
H12_PERIOD = 60 * 12
HOUR_PERIOD = 60

plt.rcParams["savefig.dpi"] = 300

if __name__ == "__main__":
    get_data_from_uci(DATA_PATH)
    X = clean_data(DATA_PATH)
    X = filter_timeseries(X, START_DATE, END_DATE)
    X = fill_missing_values(X)

    plot_timeseries(X)

    # to pandas for statsmodels
    X = X.to_pandas()
    X.set_index("datetime", inplace=True)

    # Now decompose the data
    # NOTE: using two_sided=False to avoid using future information
    weekly_decomposition = seasonal_decompose(
        X, model="additive", period=WEEK_PERIOD, two_sided=False
    )
    weekly_trend = weekly_decomposition.trend
    # weekly_decomposition.plot()
    Y = weekly_decomposition.seasonal.to_frame(name="power")

    fig, ax = plt.subplots(figsize=(24, 4))
    ax.set_xlim(np.datetime64(START_DATE), np.datetime64(END_DATE))
    ax.scatter(Y.index, Y["power"], color="red", s=0.01)
    plt.title("Weekly Seasonal")
    plt.savefig("./figs/weekly_decomposition.png")

    daily_decomposition = seasonal_decompose(
        weekly_trend.dropna(), model="additive", period=DAY_PERIOD, two_sided=False
    )
    daily_trend = daily_decomposition.trend
    Y = daily_decomposition.seasonal.to_frame(name="power")
    fig, ax = plt.subplots(figsize=(24, 4))
    ax.set_xlim(np.datetime64(START_DATE), np.datetime64(END_DATE))
    ax.scatter(Y.index, Y["power"], color="red", s=0.01)
    plt.title("Daily Seasonal")
    plt.savefig("./figs/daily_decomposition.png")

    h12_decomposition = seasonal_decompose(
        daily_trend.dropna(), model="additive", period=H12_PERIOD, two_sided=False
    )
    h12_trend = h12_decomposition.trend
    Y = h12_decomposition.seasonal.to_frame(name="power")
    fig, ax = plt.subplots(figsize=(24, 4))
    ax.set_xlim(np.datetime64(START_DATE), np.datetime64(END_DATE))
    ax.scatter(Y.index, Y["power"], color="red", s=0.01)
    plt.title("Twice Daily Seasonal")
    plt.savefig("./figs/h12_decomposition.png")

    hourly_decomposition = seasonal_decompose(
        h12_trend.dropna(), model="additive", period=HOUR_PERIOD, two_sided=False
    )
    hourly_trend = hourly_decomposition.trend
    Y = hourly_decomposition.seasonal.to_frame(name="power")
    fig, ax = plt.subplots(figsize=(24, 4))
    ax.set_xlim(np.datetime64(START_DATE), np.datetime64(END_DATE))
    ax.scatter(Y.index, Y["power"], color="red", s=0.01)
    plt.title("Hourly Seasonal")
    plt.savefig("./figs/hourly_decomposition.png")

    power = X["power"]
    residual = (
        power
        - hourly_trend
        - h12_decomposition.seasonal
        - hourly_decomposition.seasonal
        - daily_decomposition.seasonal
        - weekly_decomposition.seasonal
    )
    residual = residual.to_frame(name="power")

    fig, ax = plt.subplots(figsize=(24, 4))
    ax.set_xlim(np.datetime64(START_DATE), np.datetime64(END_DATE))
    ax.scatter(residual.index, residual["power"], color="blue", s=0.01)
    plt.title("Residual")

    plt.xlabel("Date")
    plt.ylabel("Global Active Power")

    plt.tight_layout()
    plt.savefig("./figs/residual.png")
    plt.close()

    print("Success")
