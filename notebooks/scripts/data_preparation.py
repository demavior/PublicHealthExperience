import pandas as pd

def load_data(file_path):
    """Load the CSV file with specified data types."""
    df = pd.read_csv(file_path, dtype='str')
    df['Year'] = 2023
    return df

def rename_measure_id(df):
    """Rename columns based on predefined mappings."""
    rename_mappings = {
        "H_COMP_1_": "NURSE_COMM_",
        "H_COMP_2_": "DOCTOR_COMM_",
        "H_COMP_3_": "STAFF_RESPON_",
        "H_COMP_5_": "MEDICINE_",
        "H_COMP_6_": "DISCHARGE_INFO_",
        "H_COMP_7_": "CARE_TRANSIT_",
        "H_CLEAN_HSP_": "H_CLEAN_",
        "H_QUIET_HSP_": "H_QUIET_"
    }
    df["HCAHPS Measure ID"] = df["HCAHPS Measure ID"].replace(rename_mappings, regex=True)
    return df

def create_value_column(df):
    """Create 'HCAHPS Answer' column based on conditions."""
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

def clean_pivot_data(pivot_df):
    """Clean the pivoted data."""
    # Replace 'Not Available' with NA
    pivot_df.replace("Not Available", pd.NA, inplace=True)
    # Convert columns to numeric
    numeric_col_names=pivot_df.iloc[:, 8:].columns
    pivot_df[numeric_col_names] = pivot_df[numeric_col_names].astype('Int64')
    
    return pivot_df

def exclude_nulls(pivot_df):
    """Exclude facilities with null values."""
    cleaned_pivot_df = pivot_df[~pivot_df['Number of Completed Surveys'].isnull()]
    cleaned_pivot_df = cleaned_pivot_df[cleaned_pivot_df['Number of Completed Surveys'] > 50]
    cleaned_pivot_df = cleaned_pivot_df[cleaned_pivot_df['H_NURSE_RESPECT_A_P'].notnull()]
    return cleaned_pivot_df

def calculate_linear_scores(cleaned_pivot_df):
    """Calculate linear scores and fill NA values."""
    linear_score_comparison = pd.DataFrame()
    # Iterate through each feature to calculate linear score
    for feature in [col.split('_LINEAR_SCORE')[0] for col in cleaned_pivot_df.columns if col.endswith('_LINEAR_SCORE')]:
        # Calculate linear score based on feature
        if feature == 'DISCHARGE_INFO':
            calculated_linear_score = cleaned_pivot_df['DISCHARGE_INFO_Y_P'].round()
        elif feature == 'H_HSP_RATING':
            calculated_linear_score = (cleaned_pivot_df[f'{feature}_0_6'] * 0.45 +
                                       cleaned_pivot_df[f'{feature}_7_8'] * 0.8 +
                                       cleaned_pivot_df[f'{feature}_9_10'] * 0.95).round()
        else:
            if f'{feature}_A_P' in cleaned_pivot_df.columns:
                A_P_column = f'{feature}_A_P'
                U_P_column = f'{feature}_U_P'
                SN_P_column = f'{feature}_SN_P'
            elif f'{feature}_SA' in cleaned_pivot_df.columns:
                A_P_column = f'{feature}_SA'
                U_P_column = f'{feature}_A'
                SN_P_column = f'{feature}_D_SD'
            elif f'{feature}_DY' in cleaned_pivot_df.columns:
                A_P_column = f'{feature}_DY'
                U_P_column = f'{feature}_PY'
                SN_P_column = f'{feature}_DN'
            else:
                print(f"{feature}_AP does not exist for feature {feature}. Skipping...")
                continue

            calculated_linear_score = (cleaned_pivot_df[A_P_column] +
                                       cleaned_pivot_df[U_P_column] * 2/3 +
                                       cleaned_pivot_df[SN_P_column] * 1/6 + 0.6).round()
        # Fill NA values with calculated linear score
        ls_column = f'{feature}_LINEAR_SCORE'
        cleaned_pivot_df[ls_column]=cleaned_pivot_df[ls_column].fillna(calculated_linear_score)
        # Compare actual and calculated linear scores
        feature_comparison = pd.DataFrame({
            'Actual_Score': cleaned_pivot_df[ls_column],
            'Calculated_Score': calculated_linear_score,
            'Difference': calculated_linear_score - cleaned_pivot_df[ls_column]
        })
        
        linear_score_comparison = pd.concat([linear_score_comparison, feature_comparison], axis=0, ignore_index=True)
    print(linear_score_comparison.mean())

    return cleaned_pivot_df

def reduce_columns(cleaned_pivot_df):
    """Reduce columns to only necessary ones."""
    linear_score_columns = [col for col in cleaned_pivot_df.columns[11:] if col.endswith('LINEAR_SCORE')]
    reduced_df = pd.concat([cleaned_pivot_df.iloc[:, :11].drop(columns=cleaned_pivot_df.columns[[2, 5, 6, 7]]), 
                            cleaned_pivot_df[linear_score_columns].rename(columns=lambda x: x.replace('_LINEAR_SCORE', ''))], axis=1)
    return reduced_df

def load_state_region_data(file_path):
    """Load and prepare state region data."""
    state_region_df = pd.read_csv(file_path)
    state_region_df = state_region_df.rename(columns={"State Code": "State", "State": "Name"})
    
    us_territories = pd.DataFrame({
        "State": ["AS", "GU", "MP", "PR", "VI"],
        "Name": ["American Samoa", "Guam", "Northern Mariana Islands", "Puerto Rico", "Virgin Islands"],
        "Region": ["U.S. Territories", "U.S. Territories", "U.S. Territories", "U.S. Territories", "U.S. Territories"],
        "Division": ["U.S. Territories", "U.S. Territories", "U.S. Territories", "U.S. Territories", "U.S. Territories"]
    })
    
    state_region_df = pd.concat([state_region_df, us_territories], ignore_index=True)
    return state_region_df

def merge_state_region_data(reduced_df, state_region_df):
    """Merge state region data with the main DataFrame."""
    completed_df = pd.merge(reduced_df, state_region_df, how='left', on='State')
    completed_df = completed_df.rename(columns={"Name": "State Name"})
    return completed_df

def rename_columns_final(df):
    """Rename columns to more descriptive names."""
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
    return df

def save_to_csv(df, file_path):
    """Save the DataFrame to a CSV file."""
    df.to_csv(file_path, index=False)