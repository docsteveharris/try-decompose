# %% Setup
import matplotlib.pyplot as plt

from clean_data import clean_data, fill_missing_values, filter_timeseries
from load_data import get_data_from_uci

DATA_PATH = "./data/household_power_consumption.txt"
START_DATE = "2008-01-01"
END_DATE = "2008-01-21"
WEEK_PERIOD = 60 * 24 * 7
DAY_PERIOD = 60 * 24
HOUR_PERIOD = 60

plt.rcParams["savefig.dpi"] = 300

# %% Load data
print("Loading data...")
get_data_from_uci(DATA_PATH)
X = clean_data(DATA_PATH)
X = filter_timeseries(X, START_DATE, END_DATE)
X = fill_missing_values(X)

# %% Plot timeseries
# plot_timeseries(X)
from scipy import signal

# fs is the sampling frequency: here it is every minute
fs = 60 * 24 * 7
f, Pxx_den = signal.periodogram(X["power"], fs=fs)

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(f, Pxx_den)
ax.set_xlabel("Frequency ")
ax.set_ylabel("Power Spectral Density")
plt.title("Periodogram (Minute level data)")


# Add vertical lines for hourly and weekly frequencies
# ax.axvline(x=fs / 60, color="r", linestyle="--", alpha=0.5, label="Hourly")
ax.axvline(x=fs / (60 * 24), color="g", linestyle="--", alpha=0.5, label="Daily")
ax.axvline(x=fs / (60 * 6), color="r", linestyle="--", alpha=0.5, label="2x Daily")
ax.axvline(x=fs / (60 * 12), color="b", linestyle="--", alpha=0.5, label="4x Daily")
# ax.axvline(x=fs / (7 * 60 * 24), color="b", linestyle="--", alpha=0.5, label="Weekly")

ax.set_xscale("log")

plt.savefig("./figs/power_spectral_density.png")
plt.show()
