import pandas as pd
import numpy as np
from scipy.stats import f_oneway
from scipy.stats import kruskal

def calculate_genre_statistics(df, genres, regions_groupings):
    """
    calculate_genre_statistics - calculates mean ratings and confidence intervals for movies by genre and region.

    Inputs: - df (dataframe): the dataframe containing movie ratings and regions
            - genres (list): list of top genres to analyze
            - regions_groupings (list): list of regions to group by

    Outputs: - mean_ratings (dict): a dictionary with genres as keys and lists of mean ratings by region as values
             - confidence_intervals (dict): a dictionary with genres as keys and lists of confidence intervals by region as values
    """
    mean_ratings = {}
    confidence_intervals = {}

    for genre in genres:
        # grouping by region
        genre_mean_ratings = df[df["genres"] == genre].groupby("region")

        # getting current size
        genre_mean_ratings_size = genre_mean_ratings.size().sort_index()

        # calculating mean ratings and stderr
        genre_mean_ratings_regions_average = genre_mean_ratings.mean("averageRating").apply(lambda x: round(x*2)/2).sort_index()
        genre_mean_ratings_regions_stderr = genre_mean_ratings["averageRating"].std().sort_index() / np.sqrt(genre_mean_ratings_size)  

        # storing the mean ratings and confidence intervals for the genre
        genre_means = []
        genre_CI = []
        for region in regions_groupings:
            # cases with less than 10 movies
            if genre_mean_ratings_size.loc[region] < 10:
                mean_rating = 0.0
                CI = 0.0
            else:
                mean_rating = genre_mean_ratings_regions_average.loc[region]["averageRating"]

                # computing 95% CI assuming normal distribution
                CI = genre_mean_ratings_regions_stderr.loc[region] * 1.96

            genre_means.append(mean_rating)
            genre_CI.append(CI)

        # appending the results to the dictionaries
        mean_ratings[genre] = genre_means
        confidence_intervals[genre] = genre_CI

    return mean_ratings, confidence_intervals

def calculate_region_statistics(df, regions, top_genres):
    """
    calculate_region_statistics - calculates mean ratings and confidence intervals for movies by region and genre.

    Inputs: - df (dataframe): the dataframe containing movie ratings and genres
            - regions (list): list of regions to analyze
            - top_genres (list): list of top genres to analyze

    Outputs: - mean_ratings (dict): a dictionary with regions as keys and lists of mean ratings by genre as values
             - confidence_intervals (dict): a dictionary with regions as keys and lists of confidence intervals by genre as values
    """
    mean_ratings = {}
    confidence_intervals = {}

    for region in regions:
        # grouping by genre
        genre_mean_ratings = df[df["region"] == region].groupby("genres")

        # getting current size
        genre_mean_ratings_size = genre_mean_ratings.size().sort_index()

        # calculating mean ratings and stderr
        genre_mean_ratings_regions_average = genre_mean_ratings.mean("averageRating").apply(lambda x: round(x*2)/2).sort_index()
        genre_mean_ratings_regions_stderr = genre_mean_ratings["averageRating"].std().sort_index() / np.sqrt(genre_mean_ratings_size)

        # storing the mean ratings and confidence intervals for the region
        region_means = []
        region_CI = []
        for genre in top_genres:
            mean_rating = genre_mean_ratings_regions_average.loc[genre]["averageRating"]
            region_means.append(mean_rating)

            # computing 95% CI assuming normal distribution
            CI = genre_mean_ratings_regions_stderr.loc[genre] * 1.96
            region_CI.append(CI)

        # appending the results to the dictionaries
        mean_ratings[region] = region_means
        confidence_intervals[region] = region_CI

    return mean_ratings, confidence_intervals

def calculate_region_decade_statistics(df, regions, top_genres, decades):
    """
    calculate_region_decade_statistics - calculates mean ratings and confidence intervals for movies by genre,
    region, and decade.

    Inputs: - df (dataframe): the dataframe containing movie ratings, genres, regions, and decades
            - regions (list): list of regions to analyze
            - top_genres (list): list of top genres to analyze
            - decades (list): list of decades to categorize movies into

    Outputs: - mean_ratings (dict): a dictionary with regions as keys and 2D arrays of mean ratings (genres x decades) as values
             - confidence_intervals (dict): a dictionary with regions as keys and 2D arrays of confidence intervals (genres x decades) as values
    """
    mean_ratings = {}
    confidence_intervals = {}

    for region in regions:
        # grouping by genre and decade
        genre_mean_ratings = df[df["region"] == region].groupby(["genres", "decade"])

        # getting current size
        genre_mean_ratings_size = genre_mean_ratings.size().sort_index()

        # calculating the necessary values
        genre_mean_ratings_regions_average = genre_mean_ratings.mean("averageRating").sort_index()
        genre_mean_ratings_regions_stderr = genre_mean_ratings["averageRating"].std().sort_index() / np.sqrt(genre_mean_ratings_size)

        # initializing arrays to store the results
        region_means = np.zeros((len(top_genres), len(decades)))
        region_CI = np.zeros((len(top_genres), len(decades)))

        # looping on top_genres
        for i, genre in enumerate(top_genres):
            # looping on decades
            for j, decade in enumerate(decades):
                if genre_mean_ratings_size.loc[(genre, decade)] < 3:
                    region_means[i][j] = 0.0
                    region_CI[i][j] = 0.0
                else:
                    region_means[i][j] = genre_mean_ratings_regions_average.loc[(genre, decade), "averageRating"]
                    region_CI[i][j] = genre_mean_ratings_regions_stderr.loc[(genre, decade)] * 1.96

        # storing the results in the dictionaries
        mean_ratings[region] = region_means
        confidence_intervals[region] = region_CI

    return mean_ratings, confidence_intervals

def calculate_genre_region_decade_statistics(df, top_genres, regions, decades):
    """
    calculate_genre_region_decade_statistics - calculates the mean ratings and confidence intervals 
    for movies per region per genre over decades.

    Inputs: - df (DataFrame): the dataframe containing movie ratings by region, genre, and decade
            - top_genres (list): list of the top genres to process
            - regions (list): list of regions
            - decades (list): list of decades to evaluate

    Outputs: - mean_ratings (dict): dictionary containing mean ratings per region and genre per decade
             - confidence_intervals (dict): dictionary containing the 95% confidence intervals per region and genre per decade
    """
    # defining dictionaries to store the results
    mean_ratings = {}
    confidence_intervals = {}

    # looping through each genre to calculate mean ratings and confidence intervals per region per decade
    for genre in top_genres:
        genre_df = df[df["genres"] == genre]

        # grouping by region and decade
        region_mean_ratings = genre_df.groupby(["region", "decade"])

        # getting current size
        region_mean_ratings_size = region_mean_ratings.size().sort_index()

        # calculating mean ratings and standard error
        region_mean_ratings_regions_average = region_mean_ratings.mean("averageRating").sort_index()
        region_mean_ratings_regions_stderr = region_mean_ratings["averageRating"].std().sort_index() / np.sqrt(region_mean_ratings_size)

        # initializing arrays to store the results for each region and decade
        region_means = np.zeros((len(regions), len(decades)))
        region_CI = np.zeros((len(regions), len(decades)))

        # looping over each region and decade to fill in the statistics
        for i, region in enumerate(regions):
            for j, decade in enumerate(decades):
                if region_mean_ratings_size.loc[(region, decade)] < 3:
                    region_means[i][j] = 0.0
                    region_CI[i][j] = 0.0
                else:
                    region_means[i][j] = region_mean_ratings_regions_average.loc[(region, decade), "averageRating"]
                    region_CI[i][j] = region_mean_ratings_regions_stderr.loc[(region, decade)] * 1.96

        # storing the results in the dictionaries
        mean_ratings[genre] = region_means
        confidence_intervals[genre] = region_CI

    return mean_ratings, confidence_intervals

def calculate_genre_anova_p_values(df, top_genres, regions):
    """
    calculate_genre_anova_p_values - computes ANOVA p-values for average ratings of genres across regions.

    Inputs: - df (DataFrame): DataFrame containing columns 'genres', 'region', and 'averageRating'
            - top_genres (list): list of top genres to analyze
            - regions (list): list of regions names
        
    Outputs: - p_values (dict): dictionary mapping each genre to its ANOVA p-value (or None if data is insufficient)
    """
    # initializing dictionary to store p-values
    p_values = {}

    # looping through each genre
    for genre in top_genres:
        # taking current genre dataframe
        genre_df = df[df["genres"] == genre]

        # collecting ratings for each region
        region_ratings = {}
        for region in regions:
            region_ratings[region] = genre_df[genre_df["region"] == region]["averageRating"].to_list()

        # checking if all regions have non-zero ratings
        if all(len(ratings) > 0 and all(rating != 0.0 for rating in ratings) for ratings in region_ratings.values()):
            
            # performing ANOVA
            result = f_oneway(*region_ratings.values())
            p_values[str(genre)] = result[1]
        else:
            # store None if lack of data
            p_values[str(genre)] = None

    return p_values

def analyze_genre_ratings_by_region(df, regions):
    """
    analyze_genre_ratings_by_region - performs the Kruskal-Wallis test on average ratings of genres within each region.

    Inputs: - df (DataFrame): DataFrame containing columns 'region', 'genres', and 'averageRating'
            - regions (list): list of regions

    Outputs: - prints the Kruskal-Wallis statistic, p-value, and conclusions for each region
    """
    # looping through each region
    for region in regions:
        print(f"Results for region: {region}")
        
        # dividing the data for the region
        df_region = df[df['region'] == region]
        
        # collecting ratings for each genre
        genre_groups = []

        # grouping the regional movies by genres
        for genre, group in df_region.groupby('genres'):
            # extracting the ratings column for the current genre and append it as an array to the list of genre ratings
            ratings = group['averageRating'].values
            genre_groups.append(ratings)

        # performing the Kruskal-Wallis test across the genres by unpacking each list of ratings per genre
        if len(genre_groups) > 1:
            stat, p_value = kruskal(*genre_groups)
            print(f"Kruskal-Wallis Statistic: {stat:.4f}, p-value: {p_value:.4f}")
            
            # checking the significance threshold
            if p_value < 0.05:
                print(f"The null hypothesis is rejected; there is a suggested statistically significant difference in movie ratings by genre for movies in {region}.")
            else:
                print(f"The null hypothesis is failed to be rejected and a statistically significant difference in ratings across genres cannot be claimed for movies in {region}.")
        
        # printing results in a nice way
        print("\n" + "-"*50 + "\n")

def calculate_slopes(df, group_by_columns, sort_by_column, value_column):
    """
    calculate_slopes - calculates the slopes of average ratings between consecutive periods for movies grouped by specified columns.

    Inputs: - df (DataFrame): DataFrame containing the data to analyze
            - group_by_columns (list): list of column names to group by (e.g., ['region', 'genres'])
            - sort_by_column (str): column name to sort by within each group (e.g., 'decade')
            - value_column (str): column name whose mean is calculated and used for slope computation (e.g., 'averageRating')

    Outputs: - slopes_df (DataFrame): DataFrame containing the slopes between consecutive periods for each group
    """
    slopes_data = []

    # grouping by the specified columns
    for group_keys, group in df.groupby(group_by_columns):
        group = group.sort_values(sort_by_column)  # Sort by the specified column
        
        # grouping by the sort column and calculate the mean value
        group_means = group.groupby(sort_by_column)[value_column].mean().reset_index()

        # looping through consecutive periods
        for i in range(1, len(group_means)):
            period1 = group_means.iloc[i-1]
            period2 = group_means.iloc[i]
            
            # calculating slope between two consecutive periods
            slope = (period2[value_column] - period1[value_column]) / (period2[sort_by_column] - period1[sort_by_column])
            
            # storing results
            result = {col: key for col, key in zip(group_by_columns, group_keys)}
            result.update({
                f'{sort_by_column}1': period1[sort_by_column],
                f'{sort_by_column}2': period2[sort_by_column],
                'slope': slope
            })
            slopes_data.append(result)

    # converting slopes_data to DataFrame
    return pd.DataFrame(slopes_data)

def identify_top_worst_genres(slopes_df):
    """
    identify_top_worst_genres - identifies the genres with the steepest and shallowest slope in ratings 
    for each region and consecutive decade pair.

    Inputs: - slopes_df (DataFrame): DataFrame containing columns 'region', 'decade1', 'decade2', 'genre', and 'slope'

    Outputs: - top_worst_df (DataFrame): DataFrame containing the following columns:
                - region: The region analyzed
                - decade1: The start of the consecutive decade pair
                - decade2: The end of the consecutive decade pair
                - top_genre: Genre with the steepest positive slope
                - top_slope: Value of the steepest positive slope
                - worst_genre: Genre with the most negative slope
                - worst_slope: Value of the most negative slope
    """
    top_worst_data = []

    # grouping by region
    for region, group in slopes_df.groupby('region'):
        # grouping by consecutive decades within the region
        for decade_pair, decade_group in group.groupby(['decade1', 'decade2']):
            # finding top and worst genres within the current decade pair
            top_genre = decade_group.loc[decade_group['slope'].idxmax()]
            worst_genre = decade_group.loc[decade_group['slope'].idxmin()]

            # storing the results
            top_worst_data.append({
                'region': region,
                'decade1': decade_pair[0],
                'decade2': decade_pair[1],
                'top_genre': top_genre['genres'],
                'top_slope': top_genre['slope'],
                'worst_genre': worst_genre['genres'],
                'worst_slope': worst_genre['slope']
            })

    # converting top_worst_data to a DataFrame
    return pd.DataFrame(top_worst_data)

def anova_on_slopes(df, top_genres, regions):
    """
    Performs ANOVA and Kruskal-Wallis tests on the slopes of average ratings between different decades
    for specified genre-region combinations, including detailed results of normality, homoscedasticity,
    and statistical tests.

    Inputs: 
        - df (DataFrame): DataFrame containing columns 'genres', 'region', 'decade', and 'averageRating'
        - top_genres (list): list of top genres to analyze
        - regions (list): list of regions to analyze

    Outputs: 
        - results_df (DataFrame): DataFrame containing:
            - genre: The genre analyzed
            - region: The region analyzed
            - f_stat: F-statistic from ANOVA
            - anova_p_value: P-value from ANOVA
            - kruskal_stat: Kruskal-Wallis test statistic
            - kruskal_p_value: P-value from Kruskal-Wallis test
            - significant_anova: Boolean indicating whether ANOVA p-value < 0.05
            - significant_kruskal: Boolean indicating whether Kruskal-Wallis p-value < 0.05
        - significant_results_df (DataFrame): Subset of results_df with significant results for either test
    """
    results = []

    for genre in top_genres:
        for region in regions:
            # Filter data for the current genre-region combination
            subset_df = df[(df['genres'] == genre) & (df['region'] == region)]
            
            # Group ratings by decade
            groups = [group['averageRating'].values for _, group in subset_df.groupby('decade')]
            
            # Ensure we have at least two groups with more than one data point
            if len(groups) >= 2 and all(len(g) > 1 for g in groups):
    
                # Perform ANOVA
                try:
                    f_stat, anova_p_value = f_oneway(*groups)
                except ValueError:
                    f_stat, anova_p_value = None, None

                # Perform Kruskal-Wallis Test (non-parametric alternative to ANOVA)
                try:
                    kruskal_stat, kruskal_p_value = kruskal(*groups)
                except ValueError:
                    kruskal_stat, kruskal_p_value = None, None

                results.append({
                    'genre': genre,
                    'region': region,
                    'f_stat': f_stat,
                    'anova_p_value': anova_p_value,
                    'kruskal_stat': kruskal_stat,
                    'kruskal_p_value': kruskal_p_value,
                    'significant_anova': anova_p_value < 0.05 if anova_p_value is not None else False,
                    'significant_kruskal': kruskal_p_value < 0.05 if kruskal_p_value is not None else False
                })
            else:
                # Not enough data for tests
                results.append({
                    'genre': genre,
                    'region': region,
                    'f_stat': None,
                    'anova_p_value': None,
                    'kruskal_stat': None,
                    'kruskal_p_value': None,
                    'significant_anova': False,
                    'significant_kruskal': False
                })

    # Convert results to DataFrame
    results_df = pd.DataFrame(results)

    # Filter significant results
    significant_results_df = results_df[(results_df['significant_anova'] == True) | (results_df['significant_kruskal'] == True)]

    return results_df, significant_results_df


