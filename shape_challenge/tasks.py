"""
Task definitions for the data flow. This is where the actual work is done.
(This is where the magic happens.)
"""

from pathlib import Path
import shutil
from typing import Any, List

import pandas as pd
from prefect import task
import requests

from shape_challenge.logging import (
    log,
)
from shape_challenge.parsing import (
    parse_equipment_sensors_relationship,
    parse_failure_logs,
)
from shape_challenge.transform import (
    filter_range,
    merge_data,
)


@task(nout=3)
def download_data(
    url_or_path: str,
    directory_prefix: str = None,
) -> str:
    """
    Downloads a file to `/tmp/<directory_prefix>/<filename>`.
    The directory is created if it does not exist.

    Args:
        url (str): URL to the file.
        directory_prefix (str, optional): Prefix for the directory.

    Returns:
        The path to the downloaded file.
    """
    # Check if it's a file or a URL
    if Path(url_or_path).is_file():
        # It's a file, let's just copy it to a temporary directory
        filename = Path(url_or_path).name
        filepath = Path(f"/tmp/{directory_prefix}/{filename}")
        filepath.parent.mkdir(parents=True, exist_ok=True)
        log(f"Copying {url_or_path} to {filepath}")
        shutil.copy(url_or_path, filepath)
    else:
        # Splits URL and gets filename
        filename: str = url_or_path.split("/")[-1]

        # Adds prefix to directory name if given
        if directory_prefix is not None:
            directory = Path(f"/tmp/{directory_prefix}")
        else:
            directory = Path("/tmp")

        # Creates directory if it does not exist
        directory.mkdir(parents=True, exist_ok=True)
        filepath = directory / filename

        # Downloads file
        log(f"Downloading file from {url_or_path} to {filepath}...")
        response = requests.get(url_or_path)

        # Saves file to directory
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(response.text)

    return str(filepath)


@task(checkpoint=False)
def filter_data(
    dataframe: pd.DataFrame,
    filter_column: str,
    range_start: float,
    range_end: float,
) -> pd.DataFrame:
    """
    Filters a range within a dataframe column.

    Args:
        dataframe (pd.DataFrame): Dataframe to filter.
        filter_column (str): Column to filter.
        range_start (float): Minimum value for the range.
        range_end (float): Maximum value for the range.

    Returns:
        A filtered dataframe.
    """
    log(
        f"Filtering dataframe by {filter_column} and range [{range_start}, {range_end}]")
    return filter_range(dataframe, filter_column, range_start, range_end)


@task
# pylint: disable=too-many-arguments
def generate_report(
    output_file_path: str,
    total_failures: int,
    most_failures_equipment_code: str,
    average_failures_across_equipment_groups: pd.DataFrame,
    range_min: str,
    range_max: str,
) -> str:
    """
    Generates a report and save it locally.

    Args:
        total_failures (int): Total number of failures.
        most_failures_equipment_code (str): Equipment code with the most failures.
        average_failures_across_equipment_groups (pd.DataFrame): Average failures
            across equipment groups.

    Returns:
        The report text.
    """
    log("Generating report...")
    report = ""
    report += f">>> Report of failures between {range_min} and {range_max} <<<\n"
    report += f"- Total number of failures: {total_failures}\n"
    report += f"- Equipment code with the most failures: {most_failures_equipment_code}\n"
    report += "- Average failures across equipment groups:\n"
    for _, row in average_failures_across_equipment_groups.iterrows():
        report += f"\t* {row['equipment_group_name']}: {row['average_failures']}\n"
    output_file = Path(output_file_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(report)
    return report


@task(checkpoint=False)
def get_average_failures_across_equipment_groups(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Gets the average number of failures for each equipment group, ordered
    by the number of failures in ascending order.

    Args:
        dataframe (pd.DataFrame): Dataframe to filter.

    Returns:
        A dataframe with the average number of failures for each
        equipment group.
    """
    # Count equipments per group
    dataframe_count = dataframe.groupby("equipment_group_name"
                                        ).agg({"equipment_code": "nunique"}).rename(
        columns={"equipment_code": "equipment_count"}).reset_index()

    # Count failures per group
    dataframe_failures = dataframe.groupby("equipment_group_name"
                                           ).count()[["sensor_id"]].rename(
        columns={"sensor_id": "failure_count"}).reset_index()

    # Merge dataframes
    dataframe_merged = pd.merge(dataframe_count, dataframe_failures,
                                on="equipment_group_name")

    # Calculate average failures per group
    dataframe_merged["average_failures"] = dataframe_merged[
        "failure_count"] / dataframe_merged["equipment_count"]

    # Sort by average failures
    dataframe_merged = dataframe_merged.sort_values(
        by="average_failures", ascending=True)

    # Remove extra columns
    dataframe_merged = dataframe_merged.drop(
        columns=["equipment_count", "failure_count"])

    log("The average number of failures for each equipment group is:")
    log(dataframe_merged)

    return dataframe_merged


@task
def get_most_failures_equipment_code(
    dataframe: pd.DataFrame,
) -> str:
    """
    Gets the equipment code with the most failures.

    Args:
        dataframe (pd.DataFrame): Dataframe to filter.

    Returns:
        The equipment code with the most failures.
    """
    code = dataframe.groupby("equipment_code").count()[
        "sensor_id"].idxmax()
    log(f"The equipment code with the most failures is {code}")
    return code


@task
def get_total_equipment_failures(
    dataframe: pd.DataFrame,
) -> int:
    """
    Returns the total number of equipment failures.

    Args:
        dataframe (pd.DataFrame): Dataframe with the equipment failures.

    Returns:
        The total number of equipment failures.
    """
    total = dataframe.shape[0]
    log(f"Total number of equipment failures: {total}")
    return total


@task
def is_none(
    value: Any,
) -> bool:
    """
    Checks if a value is None.

    Args:
        value (Any): Value to check.

    Returns:
        True if the value is None, False otherwise.
    """
    return value is None


@task(checkpoint=False)
def load_data(
    filenames: List[str],
) -> pd.DataFrame:
    """
    Loads data from the downloaded files and returns the merged DataFrame.

    Args:
        filenames: List[str]: Filenames of the downloaded files. It must
            have length 3 and the following order:

            - failure_logs_path (str): Path to the failure logs.
            - equipment_path (str): Path to the equipment information.
            - sensor_equipment_path (str): Path to the equipments and
                sensors relationships.

    Returns:
        A tuple with the dataframes.

    Raises:
        AssertionError: If the length of the filenames is not 3.
        ValueError: If the filenames are in the wrong order.
    """
    # Checks length of filenames
    if len(filenames) != 3:
        raise AssertionError("filenames must have length 3")

    # Tries to load data. If it fails, assumes that filenames is in the
    # wrong order and raises an error.
    try:
        failure_logs = parse_failure_logs(filenames[0])
        log("Successfully parsed failure logs.")
        equipment = pd.read_json(filenames[1])
        log("Successfully parsed equipment information.")
        sensor_equipment = parse_equipment_sensors_relationship(filenames[2])
        log("Successfully parsed equipment-sensor relationships.")
    except Exception as exc:
        raise ValueError("filenames must be in the following order: "
                         "failure_logs, equipment, sensor_equipment") from exc

    # Merges data
    log("Merging dataframes and returning...")
    return merge_data(failure_logs, equipment, sensor_equipment)


@task
def send_report_to_discord(
    report_text: str,
    discord_webhook_url: str,
) -> None:
    """
    Sends the report to the Discord webhook.

    Args:
        report_text (str): The report text.
        discord_webhook_url (str): The Discord webhook URL.
    """
    log("Sending report to Discord...")
    requests.post(
        discord_webhook_url,
        data={
            "content": f"```{report_text}```"
        }
    )
