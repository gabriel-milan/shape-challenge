from shape_challenge.constants import Constants as constants
from shape_challenge.flows import flow

if __name__ == "__main__":
    flow.run(
        parameters={
            "Failure logs URL or path": constants.LOCAL_FAILURE_LOGS_PATH.value,
            "Equipment data URL or path": constants.LOCAL_EQUIPMENT_PATH.value,
            "Equipment-sensors relationship URL or path": constants.LOCAL_EQUIPMENT_SENSORS_PATH.value,
            "Start date": constants.SAMPLE_START_DATE.value,
            "End date": constants.SAMPLE_END_DATE.value,
            "Output report file path": constants.LOCAL_OUTPUT_FILE_PATH.value,
        }
    )
