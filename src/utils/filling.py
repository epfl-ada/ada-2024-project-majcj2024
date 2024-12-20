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
    
def fill_ethnicity(row, unmatched_ethnicities):
    """
    fill_ethnicity - Resolves and fills ambiguous or missing ethnicity labels in a dataset.

    Inputs: - row (Series): A Pandas Series representing a single row of a DataFrame, 
              containing 'ethnicity_label', 'nationalityLabel', and other relevant fields
            - unmatched_ethnicities (set): A set of ethnicity labels considered ambiguous 
              or unmatched, requiring resolution via the nationality label

    Outputs: - filled_value (string): A resolved value for the ethnicity label, 
                prioritized as follows:
                1. Nationality label if ethnicity is ambiguous or missing.
                2. Ethnicity label if available and not ambiguous.
                3. Falls back to 'ethnicity_label' if other fields are missing.
    """
    if row['ethnicity_label'] in unmatched_ethnicities:
        # retrieving the nationality if the ethnicity is ambiguous
        return row['nationalityLabel'] if pd.notna(row['nationalityLabel']) else (
            row['ethnicityLabel'] if pd.notna(row['ethnicityLabel']) else row['ethnicity_label'])
    else:
        # retrieving the ethnicity label associated to it or fallback to nationality
        return row['ethnicity_label'] if pd.notna(row['ethnicity_label']) else (
            row['ethnicityLabel'] if pd.notna(row['ethnicityLabel']) else row['nationalityLabel'])

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

def fill_missing_regions(df, top_genres, regions):
    """
    fill_missing_regions - fills missing region entries for each genre in the given dataframe.

    Inputs: - df (DataFrame): the dataframe containing movie ratings data by region
            - top_genres (list): list of the top genres to process
            - regions (list): list of regions

    Outputs: - df (DataFrame): the updated dataframe with missing region entries filled
    """
    # looping through each genre to check and fill missing region entries
    for genre in top_genres:
        # identifying unique regions for the current genre
        regions_with_genre = df[df["genres"] == genre]["region"].unique()

        # converting unique regions to a list
        regions_with_genre = regions_with_genre.tolist()

        # checking if the number of regions for the current genre is less than the total number of regions
        if len(regions_with_genre) < 9:
            for region in regions:
                if region not in regions_with_genre:
                    # creating a new row for the missing region and setting averageRating as 0.0
                    new_row = {"region": region, "genres": genre, "averageRating": 0.0}
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    return df

def fill_missing_decades(df, top_genres, regions, decades):
    """
    fill_missing_decades - fills missing decade entries for each genre in each region in the given dataframe.

    Inputs: - df (DataFrame): the dataframe containing movie ratings data by region and decade
            - top_genres (list): list of the top genres to process
            - regions (list): list of regions
            - decades (list): list of decades to check for missing entries

    Outputs: - df (DataFrame): the updated dataframe with missing decade entries filled
    """
    # looping through each genre to check and fill missing decade entries per region
    for genre in top_genres:
        genre_df = df[df["genres"] == genre]

        # looping over each region
        for region in regions:
            # getting unique decades for the current region and genre
            regions_with_genre_decade = genre_df[genre_df["region"] == region]["decade"].unique()

            # converting unique decades to a list
            regions_with_genre_decade = regions_with_genre_decade.tolist()

            # checking for missing decades and fill them
            if len(regions_with_genre_decade) < len(decades):
                for dec in decades:
                    if dec not in regions_with_genre_decade:
                        # creating a new row with missing decade and filling with averageRating as 0.0
                        new_row = {"region": region, "genres": genre, "averageRating": 0.0, "decade": dec}
                        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    return df