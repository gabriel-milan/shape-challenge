# pylint: disable=R0801
"""
Implementation of the data flow using Prefect. The flow is implemented using
parameters so we can assure this package is reusable.
"""

from prefect import Flow, Parameter, case

from shape_challenge.tasks import (
    download_data,
    filter_data,
    generate_report,
    get_average_failures_across_equipment_groups,
    get_most_failures_equipment_code,
    get_total_equipment_failures,
    is_none,
    load_data,
    send_report_to_discord,
)

with Flow("Shape's Hard Skill Test - Data Engineer") as flow:

    ###########################################################################
    #
    # Parameters
    #
    ###########################################################################

    # URLs to the data files
    failure_logs_url = Parameter("Failure logs URL or path")
    equipment_url = Parameter("Equipment data URL or path")
    equipment_sensors_url = Parameter(
        "Equipment-sensors relationship URL or path")

    # Date range to filter the data
    start_date = Parameter("Start date")
    end_date = Parameter("End date")

    # Report parameters
    output_file_path = Parameter("Output report file path")
    discord_webhook_url = Parameter(
        "Discord webhook URL for report", default=None)

    ###########################################################################
    #
    # Tasks section #1 - Load data
    #
    ###########################################################################

    # Download the data
    downloaded_files = download_data.map(
        [failure_logs_url, equipment_url, equipment_sensors_url])

    # Merge the data
    dataframe = load_data(filenames=downloaded_files)

    ###########################################################################
    #
    # Tasks section #2 - Filter data
    #
    ###########################################################################

    # Filter the data
    dataframe = filter_data(
        dataframe=dataframe,
        filter_column="timestamp",
        range_start=start_date,
        range_end=end_date,
    )

    ###########################################################################
    #
    # Tasks section #3 - Extract information for the report
    #
    ###########################################################################

    # Total equipment failures
    total_failures = get_total_equipment_failures(dataframe=dataframe)

    # Equipment code with the most failures
    equipment_code = get_most_failures_equipment_code(dataframe=dataframe)

    # Average failures across equipment groups
    average_failures = get_average_failures_across_equipment_groups(
        dataframe=dataframe)

    ###########################################################################
    #
    # Tasks section #4 - Generate report and save it.
    #
    ###########################################################################

    # Generate the report text and save it locally
    report_text = generate_report(
        output_file_path=output_file_path,
        total_failures=total_failures,
        most_failures_equipment_code=equipment_code,
        average_failures_across_equipment_groups=average_failures,
        range_min=start_date,
        range_max=end_date,
    )

    # Send the report to Discord if a webhook URL is provided
    with case(is_none(value=discord_webhook_url), False):
        send_report_to_discord(
            report_text=report_text,
            discord_webhook_url=discord_webhook_url,
        )
