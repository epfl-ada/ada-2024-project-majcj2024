import json
import pandas as pd

def clean_idxs(pattern):
    """
    clean_idxs - cleans patterns such as {"/m/06ppq": "Silent film", "/m/02h40lc": "English Language"}
    into ["Silent film", "English Language"].

    Inputs: - pattern (dictonary): initial pattern to be cleaned

    Outputs: - pattern (list of strings): cleaned pattern
    """
    if pd.isna(pattern) or pattern == '{}':
        return None
    else:
        dict = json.loads(pattern)
        pattern = list(dict.values())
        return pattern
    
def clean_dates(date):
    """
    clean_dates - cleans a date string to only keep the year
    as an int.

    Inputs: - date (string): date formatted as YYYY-MM-DD

    Outputs: - date (int): YYYY of the date
    """
    if pd.isna(date):
        return None
    else:
        return int(date[:4])
