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
python3 -m pip install -e .
```

And you're done!

## Getting started

For demonstration purposes, I've included sample data files in the repository.
They are located in the `sample_data/` directory. Although it follows the
same structure as the real data files, they do not contain the same data or
any of the original information.



"""
