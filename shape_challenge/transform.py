"""
General transformations to the data. Includes merging dataframes,
filtering and aggregating data.
"""

import pandas as pd


def filter_range(
    dataframe: pd.DataFrame,
    column: str,
    range_min: float,
    range_max: float,
) -> pd.DataFrame:
    """
    Filters a dataframe by a given range.

    Args:
        dataframe (pd.DataFrame): The dataframe to be filtered.
        column (str): The column to be filtered.
        range_min (float): The minimum value of the range.
        range_max (float): The maximum value of the range.

    Returns:
        A pandas dataframe with the filtered data.
    """
    return dataframe[
        (dataframe[column] >= range_min) &
        (dataframe[column] <= range_max)
    ]


def merge_data(
    dataframe_failure_logs: pd.DataFrame,
    dataframe_equipment: pd.DataFrame,
    dataframe_sensor_equipment: pd.DataFrame,
) -> pd.DataFrame:
    """
    Merges information from the three different data sources for
    this problem. This also checks that there's only the `ERROR`
    message level for each failure. If that's not the case, it
    raises an error.

    Args:
        dataframe_failure_logs (pd.DataFrame): DataFrame containing
            all failure events from the logs. Columns are:

            - timestamp (datetime): The timestamp of the failure.
            - sensor_id (int): The sensor ID.
            - message_level (str): The message level of the event.
            - temperature (float): The temperature measured by the
                sensor.
            - vibration (float): The vibration measured by the sensor.

        dataframe_equipment (pd.DataFrame): DataFrame that contains
            equipments information. Columns are:

            - equipment_id (int): The equipment identifier.
            - code (str): another identifier code for the equipment.
            - group_name (str): name of the group that the equipment
                belongs to.

        dataframe_sensor_equipment (pd.DataFrame): DataFrame that
            contains equipments and sensors relationships. Columns are:

            - equipment_id (int): The equipment identifier.
            - sensor_id (int): The sensor identifier.

    Returns:
        A pandas dataframe with the merged data. Columns are:

        - timestamp (datetime): The timestamp of the failure.
        - sensor_id (int): The sensor ID.
        - temperature (float): The temperature measured by the sensor.
        - vibration (float): The vibration measured by the sensor.
        - equipment_id (int): The equipment ID.
        - equipment_code (str): The equipment code.
        - equipment_group_name (str): The equipment group name.

    Raises:
        AssertionError: If there's a failure with a different message
            level than `ERROR`.
    """
    # Assert that all message levels are "ERROR". If that's the case, we can safely
    # remove the column.
    assert dataframe_failure_logs["message_level"].unique() == ["ERROR"]
    dataframe_failure_logs = dataframe_failure_logs.drop(
        "message_level", axis=1)

    # Merge dataframes
    dataframe = pd.merge(
        dataframe_failure_logs,
        dataframe_sensor_equipment,
        on="sensor_id",
        how="left",
    )
    dataframe = pd.merge(
        dataframe,
        dataframe_equipment,
        on="equipment_id",
        how="left",
    )

    # Rename columns
    dataframe = dataframe.rename(
        columns={
            "timestamp": "timestamp",
            "sensor_id": "sensor_id",
            "temperature": "temperature",
            "vibration": "vibration",
            "equipment_id": "equipment_id",
            "code": "equipment_code",
            "group_name": "equipment_group_name"
        }
    )

    return dataframe
