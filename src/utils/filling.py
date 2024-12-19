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
    
def fill_ethnicity(row, unmatched_ethnicities):
    """
    fill_ethnicity - Resolves and fills ambiguous or missing ethnicity labels in a dataset.

    Inputs: - row (Series): A Pandas Series representing a single row of a DataFrame, 
              containing 'ethnicity_label', 'nationalityLabel', and other relevant fields.
            - unmatched_ethnicities (set): A set of ethnicity labels considered ambiguous 
              or unmatched, requiring resolution via the nationality label.

    Outputs: - filled_value (string): A resolved value for the ethnicity label, 
                prioritized as follows:
                1. Nationality label if ethnicity is ambiguous or missing.
                2. Ethnicity label if available and not ambiguous.
                3. Falls back to 'ethnicity_label' if other fields are missing.
    """
    if row['ethnicity_label'] in unmatched_ethnicities:
        # If the ethnicity is ambiguous, retrieve the nationality
        return row['nationalityLabel'] if pd.notna(row['nationalityLabel']) else (
            row['ethnicityLabel'] if pd.notna(row['ethnicityLabel']) else row['ethnicity_label'])
    else:
        # For non-ambiguous cases, retrieve the ethnicity label associated to it or fallback to nationality
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
    # Loop through each genre to check and fill missing region entries
    for genre in top_genres:
        # Identify unique regions for the current genre
        regions_with_genre = df[df["genres"] == genre]["region"].unique()

        # Convert unique regions to a list
        regions_with_genre = regions_with_genre.tolist()

        # Check if the number of regions for the current genre is less than the total number of regions
        if len(regions_with_genre) < 9:
            for region in regions:
                if region not in regions_with_genre:
                    # Create a new row for the missing region and set averageRating as 0.0
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
    # Loop through each genre to check and fill missing decade entries per region
    for genre in top_genres:
        genre_df = df[df["genres"] == genre]

        # Loop over each region
        for region in regions:
            # Get unique decades for the current region and genre
            regions_with_genre_decade = genre_df[genre_df["region"] == region]["decade"].unique()

            # Convert unique decades to a list
            regions_with_genre_decade = regions_with_genre_decade.tolist()

            # Check for missing decades and fill them
            if len(regions_with_genre_decade) < len(decades):
                for dec in decades:
                    if dec not in regions_with_genre_decade:
                        # Create a new row with missing decade and fill with averageRating as 0.0
                        new_row = {"region": region, "genres": genre, "averageRating": 0.0, "decade": dec}
                        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    return df