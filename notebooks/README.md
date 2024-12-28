# Analysis

This directory contains the Jupyter notebooks used for data preparation, exploratory data analysis (EDA), and visualization in the Patient Satisfaction Analysis project.

## Notebooks

1. **01_data_preparation.ipynb**
   - **Description**: This notebook handles the data cleaning and preparation steps, including renaming columns, handling missing data, and adding region information.
   - **Key Steps**:
     - Import Datasets
     - Data Preparation
     - Export Processed Data

2. **02_eda.ipynb**
   - **Description**: This notebook performs exploratory data analysis to uncover patterns and insights in the data.
   - **Key Steps**:
     - Basic Data Information
     - Information by Region
     - Information by Division
     - Information by State

3. **03_visualization.ipynb**
   - **Description**: This notebook generates visualizations to illustrate the findings from the analysis.
   - **Key Steps**:
     - Correlations
     - Comparison by Regions
     - Map Visualization by States

## Scripts

`scripts/`: Directory for Python scripts. These scripts are used in the Jupyter Notebooks.
- `aggregate_data.py`: Functions for aggregating and calculating statistics.
- `calculate_data.py`: Functions for calculating data.
- `clean_data.py`: Functions for cleaning data.
- `load_data.py`: Functions for loading data.
- `map_visualization.py`: Functions for map visualizations.
- `merge_data.py`: Functions for merging data.
- `plot_functions.py`: Functions for plotting different types of visualizations.
- `save_data.py`: Functions for saving data.
- `transform_data.py`: Functions for transforming data.

## Kaggle

The entire code, including all notebooks and datasets, is also available on Kaggle. You can view and run the notebooks interactively on Kaggle:

https://www.kaggle.com/code/demavior/patient-satisfaction-in-public-healthcare

## Note

Make sure to download the raw data files from Kaggle and place them in the `data/raw` directory before running the notebooks. Detailed instructions are provided in the `data/raw/README.md` file.
