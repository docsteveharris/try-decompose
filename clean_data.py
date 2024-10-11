import polars as pl


def clean_data(data_path):
    """
    Import just power, rename, specify data types, and deal with missing values
    """
    X = pl.read_csv(
        data_path,
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

    return X


def filter_timeseries(X, start_date, end_date):
    # Subset the data to the desired date range
    start_date = pl.lit(start_date).str.to_datetime()
    end_date = pl.lit(end_date).str.to_datetime()

    return X.filter(pl.col("datetime").is_between(start_date, end_date))


def fill_missing_values(X):
    # Fill missing values with the previous non-missing value
    if X["power"].null_count() > 0:
        print(f"Number of missing rows: {X['power'].null_count()}")
        print("Filling missing values with the previous non-missing value")
    X = X.fill_null(strategy="forward")
    return X
