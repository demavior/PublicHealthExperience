import pandas as pd

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