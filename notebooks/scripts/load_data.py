import pandas as pd

def load_hospital_data(file_path):
    """Load the CSV file with specified data types."""
    df = pd.read_csv(file_path, dtype='str')
    df['Year'] = 2023
    return df

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

def load_csv_data(file_path):
    """Load a CSV data file."""
    return pd.read_csv(file_path)