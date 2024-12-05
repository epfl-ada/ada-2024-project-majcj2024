import pandas as pd

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