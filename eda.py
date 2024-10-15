import matplotlib.pyplot as plt


def plot_timeseries(X):
    # Plot the time series graph
    plt.figure(figsize=(24, 4))
    plt.scatter(X["datetime"], X["power"], color="red", s=0.01)
    # plt.xlim(X["datetime"].quantile(0.3), X["datetime"].quantile(0.7))

    plt.title("Global Active Power Over Time")
    plt.xlabel("Date")
    plt.ylabel("Global Active Power")

    plt.grid(False)
    plt.tight_layout()

    plt.savefig("./figs/timeseries.png")
    print("New plot saved to ./figs/timeseries.png")
    return plt
