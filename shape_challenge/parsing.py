"""
Gather data and clean it a little bit, just enough to use it down the road.
"""

import re
from typing import List

import pandas as pd


def parse_equipment_sensors_relationship(
    fname: str,
) -> pd.DataFrame:
    """
    Parses the CSV file that contains equipments and sensors relationships.
    As it contains a single column with both values separated by a semicolon,
    it's possible to split it into two columns and then delete the original
    one.

    Args:
        fname (str): The filename of the CSV file.

    Returns:
        A pandas dataframe with the equipments and sensors relationships.
        Columns are:

        - equipment_id (int): The equipment ID.
        - sensor_id (int): The sensor ID.
    """
    # Load data
    dataframe = pd.read_csv(fname)

    # Split columns
    dataframe["equipment_id"] = \
        dataframe["equipment_id;sensor_id"].str.split(";", expand=True)[0]
    dataframe["sensor_id"] = \
        dataframe["equipment_id;sensor_id"].str.split(";", expand=True)[1]

    # Delete original column
    dataframe = dataframe.drop("equipment_id;sensor_id", axis=1)

    # Convert column types
    dataframe["equipment_id"] = dataframe["equipment_id"].astype(int)
    dataframe["sensor_id"] = dataframe["sensor_id"].astype(int)
    return dataframe


def parse_failure_logs(
    fname: str,
) -> pd.DataFrame:
    """
    Parses the failure logs from a given file. Format of each line is:
    ```
    [<timestamp>]\t<message_level>\tsensor[<sensor_id>]:\t(temperature\t<temperature>,
        vibration\t<vibration>)
    ```

    Args:
        fname (str): The filename of the failure logs.

    Returns:
        A pandas dataframe with the failure logs. Columns are:

        - timestamp (datetime): The timestamp of the failure.
        - message_level (str): The message level of the failure.
        - sensor_id (int): The sensor ID.
        - temperature (float): The temperature measured by the sensor.
        - vibration (float): The vibration measured by the sensor.
    """
    # Open file for reading
    with open(fname, 'r') as f:
        lines: List[str] = f.readlines()

    # Parse each line
    data: List[List[str]] = []
    regex = \
        r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\t(.+?(?=\t))\tsensor\[(.+?)\]:\t\(temperature\t(.+?(?=,)), vibration\t(.+?(?=\)))"
    for line in lines:
        values = re.findall(regex, line)
        if len(values) != 1:
            raise ValueError(f"Error while parsing line: {line}")
        elif len(values[0]) != 5:
            raise ValueError(f"Error while parsing line: {line}")
        data += [values[0]]

    # Convert to dataframe
    dataframe = pd.DataFrame(
        data,
        columns=["timestamp", "message_level",
                 "sensor_id", "temperature", "vibration"]
    )

    # Convert column types
    dataframe["timestamp"] = pd.to_datetime(dataframe["timestamp"])
    dataframe["sensor_id"] = dataframe["sensor_id"].astype(int)
    dataframe["temperature"] = dataframe["temperature"].astype(float)
    dataframe["vibration"] = dataframe["vibration"].astype(float)

    return dataframe
