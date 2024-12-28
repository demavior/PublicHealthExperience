# Raw Data

This directory contains the raw data files used in the Patient Satisfaction Analysis project. The raw data files are sourced from Kaggle and include information on hospital patient satisfaction and state regions.

## Files

1. **HCAHPS-Hospital.csv**
   - **Description**: This file contains data from the Hospital Consumer Assessment of Healthcare Providers and Systems (HCAHPS) survey, which measures patients' perspectives on hospital care. This CSV file contains 447,512 raws and 23 columns.
   - **Source**: [HCAHPS-Hospital.csv](https://www.kaggle.com/datasets/demavior/patient-satisfaction-ds?select=HCAHPS-Hospital.csv)

2. **states.csv**
   - **Description**: This file contains information about the regions of different states in the United States.
   - **Source**: [states.csv](https://www.kaggle.com/datasets/demavior/patient-satisfaction-ds?select=state+regions.csv)

3. **cb_2018_us_state_500k/**
   - **Description**: This directory contains the shapefile components for the geographical data of US states, used for map visualizations.
   - **Source**: [cb_2018_us_state_500k](https://www.kaggle.com/datasets/demavior/patient-satisfaction-ds?select=cb_2018_us_state_500k)

## Usage

These raw data files are used in the project's data preparation step. They are not included in this repository due to their size. Please download the files from the provided Kaggle links and place them in this directory before running the notebooks.

## Download Instructions

1. Visit the Kaggle dataset page: https://www.kaggle.com/datasets/demavior/patient-satisfaction-ds
2. Download the following files:
   - `HCAHPS-Hospital.csv`
   - `states.csv`
   - `cb_2018_us_state_500k.zip`
3. Place the downloaded files in the `data/raw` directory.
4. Extract the `cb_2018_us_state_500k.zip` file to the `data/raw/cb_2018_us_state_500k` directory

## Note

Please make sure you have the necessary permissions and API tokens set up for Kaggle if you use the Kaggle API to programmatically download the files.
