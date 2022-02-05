"""
Constants used in the package.
"""


from enum import Enum


class Constants(Enum):
    """
    Constants used in the package. Inherits from Enum in order to forbid
    mutable values.
    """
    LOCAL_EQUIPMENT_SENSORS_PATH = ("./data/equipment_sensors.csv")
    LOCAL_EQUIPMENT_PATH = ("./data/equipment.json")
    LOCAL_FAILURE_LOGS_PATH = ("./data/equipment_failure_sensors.log")
    LOCAL_OUTPUT_FILE_PATH = (
        "./reports/shape_challenge_report.txt"
    )
    SAMPLE_END_DATE = "2020-01-31"
    SAMPLE_EQUIPMENT_SENSORS_URL = (
        "https://raw.githubusercontent.com/gabriel-milan/"
        "shape-challenge/master/sample_data/equipment_sensors.csv"
    )
    SAMPLE_EQUIPMENT_URL = (
        "https://raw.githubusercontent.com/gabriel-milan/"
        "shape-challenge/master/sample_data/equipment.json"
    )
    SAMPLE_FAILURE_LOGS_URL = (
        "https://raw.githubusercontent.com/gabriel-milan/"
        "shape-challenge/master/sample_data/equipment_failure_sensors.log"
    )
    SAMPLE_OUTPUT_FILE_PATH = (
        "./reports/sample_shape_challenge_report.txt"
    )
    SAMPLE_START_DATE = "2020-01-01"
