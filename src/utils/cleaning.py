import json
import pandas as pd
import re

# the following cleaning functions do NOT change the size of the dataframes they are applied to

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

def clean_titles(title):
    """
    clean_titles - cleans a title string to remove ' (yyyy)'.

    Inputs: - title (string): title formatted as 'title (yyy)'

    Outputs: - title (string): title formatted as 'title'
    """
    if pd.isna(title):
        return None
    else:
        title = re.sub(r"\s*\(.*\)$", "", title)
        return title

def clean_imdb(id):
    """
    clean_imdb - cleans an IMDB id string to remove 'tt' pattern.

    Inputs: - id (string): IMDB id formatted as 'tt#######'

    Outputs: - id (int): int IMDB id formatted as #######
    """
    if pd.isna(id):
        return None
    else:
        id = re.sub('tt', '', id)
        return int(id)
    
def filter_years(df, col_year, low_b=1888, up_b=2012):
    """
    filter_years - filter the column col_year of a dataframe 
    to keep the year interval [low_b, up_b].

    Inputs: - df (dataframe): dataframe to be filtered
            - col_year (string): columns on which the filtering is done
            - low_b (int): lower boundary of the years interval
            - up_b (int): upper boundary of the years interval

    Outputs: - df_filtered (dataframe): filtered dataframe
    """
    df_filtered = df[(df[col_year] >= low_b) & (df[col_year] <= up_b)]
    return df_filtered