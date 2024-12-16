import pandas as pd

def fill_iqr(df, col, t=1.5):
    """
    fill_iqr - replaces a dataframe column outliers with mean of non-outliers, 
    assuming normality and applying +/- threshold*IQR of quantiles method.

    Inputs: - df (dataframe): dataframe whose outliers should be replaced
            - col (string): considered df column
            - t (float): threshold for the IQR

    Outputs:
    """
    # calculating IQR
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    # identifying outliers and non-outliers
    outliers = df[(df[col] < Q1 - t*IQR) | (df[col] > Q3 + t*IQR)].copy()
    df = df[~((df[col] < Q1 - t*IQR) | (df[col] > Q3 + t*IQR))]

    # replacing outliers with the mean of non-outliers
    outliers[col] = df[col].mean()

    # putting fixed rows into the original dataframe
    return pd.concat([df, outliers], ignore_index=True)

def fill_col1(row, col1, col2, col3, unmatched):
    """
    fill_col1 - applied to a dataframe column, fills it 
    based on the presence of the considered feature in the unmatched variable and 
    on the values of col2, col3.

    Inputs: - row (series): dataframe row
            - col1 (string): column that needs to be filled
            - col2, col3 (string): columns on which filling is based if col1 is not unmatched
            - unmatched (list): list of unmatched strings to compare with col1

    Outputs:
    """
    if row[col1] in unmatched:
        # skip filling by keeping row[col1] as it is
        return row[col1]
    else:
        # retrieve either col2 or col3 if the first is nan
        return row[col1] if pd.notna(row[col1]) else (
            row[col2] if pd.notna(row[col2]) else row[col3])
    
def fill_historical_proximity(country, events, df):
    """
    fill_historical_proximity - applied to an historical proximity score
    df, fills its entries based on their historical proximity scores. See
    results.ipynb notebook for score definition details.

    Inputs: - country (string): current country to be filled
            - events (dictonary): contains all considered events and associated
             scores for the current country
            - df (dataframe): countries vs release_date dataframe to be filled

    Outputs: - df (dataframe): filled dataframe
    """
    # looping on events
    for event in events:
        # looping on 5 years following the current event
        for offset in range(6):
            year = event["release_date"] + offset
            if year in df.columns:
                df.loc[country, year] = round(event["score"]*max(0, 1 - 0.2*offset), 2)

    return df