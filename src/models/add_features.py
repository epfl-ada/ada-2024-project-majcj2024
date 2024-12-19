import pandas as pd
import numpy as np

def get_historical_proximity_score(row, historical_proximity_score):
    """
    get_historical_proximity_score - adds to current row the corresponding 
    historical proximity score.

    Inputs: - row (series): current dataframe row

    Outputs: - historical_proximity_score (dataframe): dataframe containing the historical
                proximity scores to be added
    """
    country = row['countries']
    release_year = row['release_date']
    
    if country in historical_proximity_score.index and release_year in historical_proximity_score.columns:
        return historical_proximity_score.loc[country, release_year]
    else:
        return None
    
def map_regions(regions):
    """
    map_regions - maps countries to the corresponding regions.

    Inputs: - region (dictionary): countries and corresponding regions

    Outputs: - country_to_region (list): mapping list
    """
    # defining output
    country_to_region = {}
    
    for region, countries in regions.items():
        for country in countries:
            country_to_region[country] = region

    return country_to_region

def get_genre_complexity_score(unique_genres_per_movie, complexity_threshold = 10):
    """
    get_genre_complexity_score - creates a mapping dictionary for each movie genre 
    complexity score, aka the number of genres that the movie has.

    Inputs: - unique_genres_per_movie (series): title-#genres associated
            - complexity_threshold (int): #genres that define the score max

    Outputs: - genre complexity score mapping dictionary
    """
    # initializing genre_complexity
    genre_complexity = np.zeros(len(unique_genres_per_movie))

    for i in range(len(unique_genres_per_movie)):
        # check threshold
        if unique_genres_per_movie.iloc[i] >= complexity_threshold:
            genre_complexity[i] = 1
        else:
            genre_complexity[i] = unique_genres_per_movie.iloc[i]/complexity_threshold

    # returning mapping dictionary
    return dict(zip(unique_genres_per_movie.index, genre_complexity))