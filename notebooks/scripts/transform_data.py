import pandas as pd

def update_measure_id(df):
    """Update Measure ID values based on predefined mappings."""
    mappings = {
        "H_COMP_1_": "NURSE_COMM_",
        "H_COMP_2_": "DOCTOR_COMM_",
        "H_COMP_3_": "STAFF_RESPON_",
        "H_COMP_5_": "MEDICINE_",
        "H_COMP_6_": "DISCHARGE_INFO_",
        "H_COMP_7_": "CARE_TRANSIT_",
        "H_CLEAN_HSP_": "H_CLEAN_",
        "H_QUIET_HSP_": "H_QUIET_"
    }
    df["HCAHPS Measure ID"] = df["HCAHPS Measure ID"].replace(mappings, regex=True)
    return df

def add_answer_column(df):
    """Add 'HCAHPS Answer' column based on conditions."""
    def get_value(row):
        if row['HCAHPS Measure ID'].endswith('_LINEAR_SCORE'):
            return row['HCAHPS Linear Mean Value']
        elif row['HCAHPS Measure ID'].endswith('_STAR_RATING'):
            return row['Patient Survey Star Rating']
        else:
            return row['HCAHPS Answer Percent']
    
    df['HCAHPS Answer'] = df.apply(get_value, axis=1)
    return df

def pivot_data(df):
    """Pivot the data to get unique values on Measure ID."""
    pivot_cols = list(df['HCAHPS Measure ID'].unique())
    group_by = list(df.columns[:8]) + ['Number of Completed Surveys', 'Survey Response Rate Percent', 'Year']
    pivot_cols = group_by + pivot_cols
    
    pivot_df = df.pivot_table(index=group_by,
                              columns='HCAHPS Measure ID', 
                              values='HCAHPS Answer',
                              aggfunc=lambda x: x.mode().iloc[0])
    
    pivot_df.reset_index(inplace=True)
    pivot_df = pivot_df[pivot_cols]
    return pivot_df

def reduce_columns(cleaned_pivot_df):
    """Reduce columns to only necessary ones."""
    linear_score_columns = [col for col in cleaned_pivot_df.columns[11:] if col.endswith('LINEAR_SCORE')]
    reduced_df = pd.concat([cleaned_pivot_df.iloc[:, :11].drop(columns=cleaned_pivot_df.columns[[2, 5, 6, 7]]), 
                            cleaned_pivot_df[linear_score_columns].rename(columns=lambda x: x.replace('_LINEAR_SCORE', ''))], axis=1)
    return reduced_df

def rename_features(df):
    """Rename feature columns to more descriptive names."""
    rename_mappings = {
        'NURSE_COMM': 'Nurse Communication',
        'DOCTOR_COMM': 'Doctor Communication',
        'STAFF_RESPON': 'Staff Responsiveness',
        'MEDICINE': 'Medicine Communication',
        'DISCHARGE_INFO': 'Discharge Information',
        'CARE_TRANSIT': 'Care Transition',
        'H_CLEAN': 'Cleanliness',
        'H_QUIET': 'Quietness',
        'H_HSP_RATING': 'Rating Score',
        'H_RECMND': 'Recommendation'
    }
    df = df.rename(columns=rename_mappings, index=rename_mappings)
    df.set_index('Facility ID', inplace=True)
    return df