from shape_challenge.constants import Constants as constants
from shape_challenge.flows import flow

if __name__ == "__main__":
    flow.run(
        parameters={
            "Failure logs URL or path": constants.SAMPLE_FAILURE_LOGS_URL.value,
            "Equipment data URL or path": constants.SAMPLE_EQUIPMENT_URL.value,
            "Equipment-sensors relationship URL or path": constants.SAMPLE_EQUIPMENT_SENSORS_URL.value,
            "Start date": constants.SAMPLE_START_DATE.value,
            "End date": constants.SAMPLE_END_DATE.value,
            "Output report file path": constants.SAMPLE_OUTPUT_FILE_PATH.value,
        }
    )
