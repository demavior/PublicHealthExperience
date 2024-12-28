import pandas as pd

def get_df_by_region(df):
    """Get statistics by region."""
    by_region_df = df.groupby('Region').agg({
        'Number of Completed Surveys': 'mean',
        'Survey Response Rate Percent': 'mean',
        'Facility ID': 'count',
        'Nurse Communication': 'mean',
        'Doctor Communication': 'mean',
        'Staff Responsiveness': 'mean',
        'Medicine Communication': 'mean',
        'Discharge Information': 'mean',
        'Care Transition': 'mean',
        'Cleanliness': 'mean',
        'Quietness': 'mean',
        'Rating Score': 'mean',
        'Recommendation': 'mean'
    }).reset_index().rename(columns={
        'Number of Completed Surveys': 'Avg Completed Surveys',
        'Survey Response Rate Percent': 'Avg Response Rate',
        'Facility ID': 'Facilities Count'
    }).round(2)

    total_stats = by_region_df.agg({
        'Avg Completed Surveys': 'mean',
        'Avg Response Rate': 'mean',
        'Facilities Count': 'sum',
        'Nurse Communication': 'mean',
        'Doctor Communication': 'mean',
        'Staff Responsiveness': 'mean',
        'Medicine Communication': 'mean',
        'Discharge Information': 'mean',
        'Care Transition': 'mean',
        'Cleanliness': 'mean',
        'Quietness': 'mean',
        'Rating Score': 'mean',
        'Recommendation': 'mean'
    }).to_frame().transpose().round(2)

    total_stats['Region'] = 'Total'
    by_region_df = by_region_df.sort_values(by='Rating Score', ascending=False)
    by_region_df = pd.concat([by_region_df, total_stats], ignore_index=True)
    by_region_df.set_index('Region', inplace=True)
    return by_region_df

def get_df_by_division(df):
    """Get statistics by division."""
    by_division_df = df.groupby('Division').agg({
        'Number of Completed Surveys': 'mean',
        'Survey Response Rate Percent': 'mean',
        'Facility ID': 'count',
        'Nurse Communication': 'mean',
        'Doctor Communication': 'mean',
        'Staff Responsiveness': 'mean',
        'Medicine Communication': 'mean',
        'Discharge Information': 'mean',
        'Care Transition': 'mean',
        'Cleanliness': 'mean',
        'Quietness': 'mean',
        'Rating Score': 'mean',
        'Recommendation': 'mean'
    }).reset_index().rename(columns={
        'Number of Completed Surveys': 'Avg Completed Surveys',
        'Survey Response Rate Percent': 'Avg Response Rate',
        'Facility ID': 'Facilities Count'
    }).round(2)
    by_division_df = by_division_df.sort_values(by='Facilities Count', ascending=False)
    by_division_df.set_index('Division', inplace=True)
    return by_division_df

def get_df_by_state(df):
    """Get statistics by state."""
    by_state_df = df.groupby('State').agg({
        'Region': 'first',
        'State Name': 'first',
        'Number of Completed Surveys': 'mean',
        'Survey Response Rate Percent': 'mean',
        'Facility ID': 'count',
        'Nurse Communication': 'mean',
        'Doctor Communication': 'mean',
        'Staff Responsiveness': 'mean',
        'Medicine Communication': 'mean',
        'Discharge Information': 'mean',
        'Care Transition': 'mean',
        'Cleanliness': 'mean',
        'Quietness': 'mean',
        'Rating Score': 'mean',
        'Recommendation': 'mean'
    }).reset_index().rename(columns={
        'Number of Completed Surveys': 'Avg Completed Surveys',
        'Survey Response Rate Percent': 'Avg Response Rate',
        'Facility ID': 'Facilities Count'
    }).round(2)
    by_state_df = by_state_df.sort_values(by='Rating Score', ascending=False)
    by_state_df.set_index('State', inplace=True)
    return by_state_df