import pandas as pd

def merge_state_region_data(reduced_df, state_region_df):
    """Merge state region data with the main DataFrame."""
    completed_df = pd.merge(reduced_df, state_region_df, how='left', on='State')
    completed_df = completed_df.rename(columns={"Name": "State Name"})
    return completed_df