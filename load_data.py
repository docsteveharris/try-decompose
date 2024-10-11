import os
from io import BytesIO
from zipfile import ZipFile

import requests


def get_data_from_uci(file_path):
    if not os.path.exists(file_path):
        print(
            f"File {file_path} does not exist. Attempting to download from UCI repository."
        )

        try:
            url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00235/household_power_consumption.zip"
            response = requests.get(url)
            with ZipFile(BytesIO(response.content)) as zip_file:
                zip_file.extractall("./data")
            return True

        except Exception as e:
            print(f"Error downloading data: {e}")
            return False

    else:
        return True
