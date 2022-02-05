"""

## Introduction

This is a package developed for "Shape's Hard Skill Test - Data Engineer".

Here, you'll find the following sub-modules:

- `shape_challenge.constants`: Constants used in the package.
- `shape_challenge.flows`: Implementation of the data flow using Prefect.
    The flow is implemented using parameters so we can assure this package
    is reusable.
- `shape_challenge.logging`: Logging wrappers for Prefect tasks.
- `shape_challenge.parsing`: Gather data and clean it a little bit, just
    enough to use it down the road.
- `shape_challenge.tasks`: Task definitions for the data flow. This is where
    the actual work is done. (This is where the magic happens.)
- `shape_challenge.transform`: General transformations to the data. Includes
    merging dataframes, filtering and aggregating data.

## Installation

`shape_challenge` has been developed using Python 3.9.5. Other 3.x versions
are probably fine too. The installation steps are below:

- First of all, clone the repository:

```bash
git clone https://github.com/gabriel-milan/shape-challenge.git
```

- (Optional, but recommended) Create a virtual environment using a tool
    like `virtualenv` or `conda`, avoiding conflicts with other packages
    that might be installed in the system.

- Now, `cd` into the directory and install the package:

```bash
cd shape-challenge
python3 -m pip install -U .
```

And you're done!

## Getting started

### Using the sample data

For demonstration purposes, I've included sample data files in the repository.
They are located in the `sample_data/` directory. Although it follows the
same structure as the real data files, they do not contain the same data or
any of the original information.

In order to run the data flow, assuming you're on the repository root and you
have the package installed, you can run the following command:

```bash
python3 scripts/run_sample.py
```

After that, you should see the report in the `reports/` directory. The file
should be named `sample_shape_challenge_report.txt` and it should contain
the following information:

```txt
>>> Report of failures between 2020-01-01 and 2020-01-31 <<<
- Total number of failures: 3
- Equipment code with the most failures: D4C3B2A1
- Average failures across equipment groups:
	* GROUP123: 1.0
	* GROUP321: 2.0
```

### Using the real data

If you want to run the data flow using the real data, you'll need to
either download the data files from the original source and place them
in the `data/` directory or you can provide the URLs to the data files,
as we did in the sample data.

Assuming you've chosen to download the data, the directory structure
should look like this:

```txt
shape-challenge/
├── data/
│   ├── equipment_failure_sensors.log
│   ├── equipment_sensors.csv
│   ├── equipment.json
├── scripts/
│   ├── run_original_data.py
    ...
```

This way, you can run the data flow using the following command:

```bash
python3 scripts/run_original_data.py
```

Similarly, the report should be generated in the `reports/` directory.
The file should be named `shape_challenge_report.txt` and it should
contain the following information:

```txt
>>> Report of failures between 2020-01-01 and 2020-01-31 <<<
- Total number of failures: 11297
- Equipment code with the most failures: E1AD07D4
- Average failures across equipment groups:
	* VAPQY59S: 802.0
	* PA92NCXZ: 833.0
	* 9N127Z5P: 846.5
	* NQWPA8D3: 847.5
	* FGHQWR2Q: 880.75
	* Z9K1SAP4: 1116.0
```

### Extra - Discord webhook integration

The implemented flow also has optional Discord webhook integration.
In other words, if you provide a Discord webhook URL, the report will
be sent to that Discord webhook.

If you want to use this feature, you'll need to provide the URL to the
webhook in any script in the `scripts/` directory, similarlly to the
example below:

```py
if __name__ == "__main__":
    flow.run(
        parameters={
            ...
            "Discord webhook URL for report": "https://discordapp.com/api/webhooks/...",
        }
    )
```

## How this was developed

The initial step was opening the data files and understanding the structure
of the data and relationships between the files. Then, I started coding
parsers for the data files in order to provide a clean and structured
pandas dataframe.

The next step was to write functions that would merge all the dataframes
together and filter the data. This way, data would be ready for any
analysis or visualization that might be needed.

Then, in order to accomplish the goal of the challenge, I started writing
the tasks that would do the actual work that the challenge required. I've
chosen Prefect for this task because it's a great tool for data pipelines
and I've got experience with it.

Finally, I've coded scripts that would run the data flow and generate
the report. The answers to the challenge are in the `reports/` directory,
but also shown [above](#using-the-real-data).

I've decided not to upload the original data files to GitHub because I
wasn't sure if it would be fine to do so.

When everything was done, I've decided to do my own exploratory analysis
and visualization of the data. Everything related to this analysis is
in the `analysis/` directory. Documentation, insights and conclusions
are also inside those files.

And that's it! Feel free to check out the code and the analysis. If you
have any questions, feel free to contact me at any time.

"""
