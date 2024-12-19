import pandas as pd
import numpy as np
from scipy.stats import f_oneway

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
        # Group by region
        genre_mean_ratings = df[df["genres"] == genre].groupby("region")

        # getting current size
        genre_mean_ratings_size = genre_mean_ratings.size().sort_index()

        # calculating mean ratings and stderr
        genre_mean_ratings_regions_average = genre_mean_ratings.mean("averageRating").apply(lambda x: round(x*2)/2).sort_index()
        genre_mean_ratings_regions_stderr = genre_mean_ratings["averageRating"].std().sort_index() / np.sqrt(genre_mean_ratings_size)  

        # Store the mean ratings and confidence intervals for the genre
        genre_means = []
        genre_CI = []
        for region in regions_groupings:
            # Handle cases with less than 10 movies
            if genre_mean_ratings_size.loc[region] < 10:
                mean_rating = 0.0
                CI = 0.0
            else:
                mean_rating = genre_mean_ratings_regions_average.loc[region]["averageRating"]

                # compute CI assuming normal distribution
                CI = genre_mean_ratings_regions_stderr.loc[region] * 1.96

            genre_means.append(mean_rating)
            genre_CI.append(CI)

        # Append the results to the dictionaries
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
        # Group by genre
        genre_mean_ratings = df[df["region"] == region].groupby("genres")

        # getting current size
        genre_mean_ratings_size = genre_mean_ratings.size().sort_index()

        # calculate mean ratings and stderr
        genre_mean_ratings_regions_average = genre_mean_ratings.mean("averageRating").apply(lambda x: round(x*2)/2).sort_index()
        genre_mean_ratings_regions_stderr = genre_mean_ratings["averageRating"].std().sort_index() / np.sqrt(genre_mean_ratings_size)

        # Store the mean ratings and confidence intervals for the region
        region_means = []
        region_CI = []
        for genre in top_genres:
            mean_rating = genre_mean_ratings_regions_average.loc[genre]["averageRating"]
            region_means.append(mean_rating)

            # Calculate the 95% confidence interval (mean +/- 1.96 * stderr assuming normal distribution)
            CI = genre_mean_ratings_regions_stderr.loc[genre] * 1.96
            region_CI.append(CI)

        # Append the results to the dictionaries
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
        # Group by genre and decade
        genre_mean_ratings = df[df["region"] == region].groupby(["genres", "decade"])

        # getting current size
        genre_mean_ratings_size = genre_mean_ratings.size().sort_index()

        # calculate the necessary values
        genre_mean_ratings_regions_average = genre_mean_ratings.mean("averageRating").sort_index()
        genre_mean_ratings_regions_stderr = genre_mean_ratings["averageRating"].std().sort_index() / np.sqrt(genre_mean_ratings_size)

        # Initialize arrays to store the results
        region_means = np.zeros((len(top_genres), len(decades)))
        region_CI = np.zeros((len(top_genres), len(decades)))

        # loop on top_genres
        for i, genre in enumerate(top_genres):
            # loop on decades
            for j, decade in enumerate(decades):
                if genre_mean_ratings_size.loc[(genre, decade)] < 3:
                    region_means[i][j] = 0.0
                    region_CI[i][j] = 0.0
                else:
                    region_means[i][j] = genre_mean_ratings_regions_average.loc[(genre, decade), "averageRating"]
                    region_CI[i][j] = genre_mean_ratings_regions_stderr.loc[(genre, decade)] * 1.96

        # Store the results in the dictionaries
        mean_ratings[region] = region_means
        confidence_intervals[region] = region_CI

    return mean_ratings, confidence_intervals

def calculate_genre_region_decade_statistics(df, top_genres, regions, decades):
    """
    calculate_genre_region_decade_statistics - calculates the mean ratings and confidence intervals 
    for movies per region per genre over decades.

    Inputs: - df (DataFrame): The dataframe containing movie ratings by region, genre, and decade
            - top_genres (list): List of the top genres to process
            - regions (list): List of regions
            - decades (list): List of decades to evaluate

    Outputs: - mean_ratings (dict): Dictionary containing mean ratings per region and genre per decade
             - confidence_intervals (dict): Dictionary containing the 95% confidence intervals per region and genre per decade
    """
    # Dictionaries to store the results
    mean_ratings = {}
    confidence_intervals = {}

    # Loop through each genre to calculate mean ratings and confidence intervals per region per decade
    for genre in top_genres:
        genre_df = df[df["genres"] == genre]

        # Group by region and decade
        region_mean_ratings = genre_df.groupby(["region", "decade"])

        # getting current size
        region_mean_ratings_size = region_mean_ratings.size().sort_index()

        # calculate mean ratings and standard error
        region_mean_ratings_regions_average = region_mean_ratings.mean("averageRating").sort_index()
        region_mean_ratings_regions_stderr = region_mean_ratings["averageRating"].std().sort_index() / np.sqrt(region_mean_ratings_size)

        # Initialize arrays to store the results for each region and decade
        region_means = np.zeros((len(regions), len(decades)))
        region_CI = np.zeros((len(regions), len(decades)))

        # Loop over each region and decade to fill in the statistics
        for i, region in enumerate(regions):
            for j, decade in enumerate(decades):
                if region_mean_ratings_size.loc[(region, decade)] < 3:
                    region_means[i][j] = 0.0
                    region_CI[i][j] = 0.0
                else:
                    region_means[i][j] = region_mean_ratings_regions_average.loc[(region, decade), "averageRating"]
                    region_CI[i][j] = region_mean_ratings_regions_stderr.loc[(region, decade)] * 1.96

        # Store the results in the dictionaries
        mean_ratings[genre] = region_means
        confidence_intervals[genre] = region_CI

    return mean_ratings, confidence_intervals

def calculate_genre_anova_p_values(df, top_genres, regions):
    """
    calculate_genre_anova_p_values - Computes ANOVA p-values for average ratings of genres across regions.

    Inputs: - df (DataFrame): DataFrame containing columns 'genres', 'region', and 'averageRating'
            - top_genres (list): List of top genres to analyze
            - regions (list): List of regions names
        
    Outputs: - p_values (dict): Dictionary mapping each genre to its ANOVA p-value (or None if data is insufficient)
    """
    # Initialize the dictionary to store p-values
    p_values = {}

    # Loop through each genre
    for genre in top_genres:
        # taking current genre dataframe
        genre_df = df[df["genres"] == genre]

        # Collect ratings for each region
        region_ratings = {}
        for region in regions:
            region_ratings[region] = genre_df[genre_df["region"] == region]["averageRating"].to_list()

        # Check if all regions have non-zero ratings
        if all(len(ratings) > 0 and all(rating != 0.0 for rating in ratings) for ratings in region_ratings.values()):
            
            # Perform ANOVA
            result = f_oneway(*region_ratings.values())
            p_values[str(genre)] = result[1]
        else:
            # If any region lacks data, store None
            p_values[str(genre)] = None

    return p_values

def analyze_genre_ratings_by_region(df, regions):
    """
    analyze_genre_ratings_by_region - Performs the Kruskal-Wallis test on average ratings of genres within each region.

    Inputs: - df (DataFrame): DataFrame containing columns 'region', 'genres', and 'averageRating'
            - regions (list): List of regions

    Outputs: - Prints the Kruskal-Wallis statistic, p-value, and conclusions for each region
    """
    from scipy.stats import kruskal

    # Looping through each region
    for region in regions:
        print(f"Results for region: {region}")
        
        # Dividing the data for the region
        df_region = df[df['region'] == region]
        
        # Collecting ratings for each genre
        genre_groups = []

        # Grouping the regional movies by genres
        for genre, group in df_region.groupby('genres'):
            # Extracting the ratings column for the current genre and append it as an array to the list of genre ratings
            ratings = group['averageRating'].values
            genre_groups.append(ratings)

        # Performing the Kruskal-Wallis test across the genres by unpacking each list of ratings per genre
        if len(genre_groups) > 1:
            stat, p_value = kruskal(*genre_groups)
            print(f"Kruskal-Wallis Statistic: {stat:.4f}, p-value: {p_value:.4f}")
            
            # Checking the significance threshold
            if p_value < 0.05:
                print(f"The null hypothesis is rejected; there is a suggested statistically significant difference in movie ratings by genre for movies in {region}.")
            else:
                print(f"The null hypothesis is failed to be rejected and a statistically significant difference in ratings across genres cannot be claimed for movies in {region}.")
        
        # Formatting in a clear way
        print("\n" + "-"*50 + "\n")