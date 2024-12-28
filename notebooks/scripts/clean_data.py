import pandas as pd

def clean_pivot_data(df):
    """Clean the pivoted data."""
    # Replace 'Not Available' with NA
    df.replace("Not Available", pd.NA, inplace=True)
    # Convert columns to numeric
    numeric_col_names=df.iloc[:, 8:].columns
    df[numeric_col_names] = df[numeric_col_names].astype('Int64')
    return df

def exclude_nulls(df):
    """Exclude facilities with null values."""
    cleaned_df = df[~df['Number of Completed Surveys'].isnull()]
    cleaned_df = cleaned_df[cleaned_df['Number of Completed Surveys'] > 50]
    cleaned_df = cleaned_df[cleaned_df['H_NURSE_RESPECT_A_P'].notnull()]
    return cleaned_df