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

def drop_most_missing(df, cols):
    """
    drop_most_missing - drops rows of a dataframe that contain the most 
    amount of missing values among features, after grouping by cols. Note that
    additional cleaning might be required as rows with the same amount of missing 
    values are kept.

    Inputs: - df (dataframe): dataframe to be cleaned
            - cols (list): columns on which the groupby operation is conducted

    Outputs: - df_cleaned (dataframe): cleaned dataframe
    """
    # count missing values occurances
    df['missing_values'] = df.isnull().sum(axis=1)

    # for each element in cols find the row with the least missing values
    df_cleaned = df.loc[df.groupby(cols)['missing_values'].idxmin()]

    # dropping 'missing_values' column
    df_cleaned = df_cleaned.drop(columns=['missing_values'])
    
    return df_cleaned

def count_entries(df, col):
    """
    count_entries - given a dataframe and one of its columns where entries are lists
    of strings, the function counts how many elements are present in each entry. Then, 
    it returns the percentages of 1-element lists over all entries.

    Inputs: - df (dataframe): dataframe to be cleaned
            - col (string): considered column

    Outputs: - perc_1 (float): percentage of entries with 1-element lists
             - entries_1 (dataframe): subset of the initial dataframe with 1-element entries
    """
    # counting elements
    df['counts'] = df[col].str.len()

    # retrieving 1-element and more than 1-element entries
    entries_1 = df[df['counts'] == 1.0]

    size_1 = entries_1.size
    total = df.size

    perc_1 = size_1/total
    
    return perc_1, entries_1

def evaluate_genre_counts(df, col, max_range):
    """
    evaluate_genre_counts - evaluates percentages of movies with a specific range of genre counts
    and subsets the data for those counts.

    Inputs: - df (dataframe): the dataframe to analyze
            - col (string): the column containing lists (e.g., genres)
            - max_range (int): the maximum number of genres to evaluate (e.g., up to 6 genres)

    Outputs: - percentages (dict): a dictionary with ranges as keys and percentages as values
             - subsets (dict): a dictionary with ranges as keys and dataframes as values
    """
    # Initialize dictionaries to store results
    percentages = {}
    subsets = {}

    # Calculate the count of genres
    df['genre_count'] = df[col].str.len()

    # Loop through the range to calculate percentages and filter subsets
    for i in range(1, max_range + 1):
        condition = df['genre_count'] <= i
        subset = df[condition]
        percentage = subset.size / df.size
        
        subsets[f"1_to_{i}_genre"] = subset
        percentages[f"1_to_{i}_genre"] = percentage

    return percentages, subsets

def categorize_decade(release_date):
    """
    categorize_decade - categorizes a movie's release year into a specific decade.

    Inputs: - release_date (int or float): the release year of the movie to be categorized

    Outputs: - (str or None): the decade to which the release year belongs (e.g., '1950', '1960', etc.), or None if it doesn't fit the specified range
    """
    if 1950 <= release_date < 1960:
        return '1950'
    elif 1960 <= release_date < 1970:
        return '1960'
    elif 1970 <= release_date < 1980:
        return '1970'
    elif 1980 <= release_date < 1990:
        return '1980'
    elif 1990 <= release_date < 2000:
        return '1990'
    elif 2000 <= release_date < 2010:
        return '2000'
    else:
        return None