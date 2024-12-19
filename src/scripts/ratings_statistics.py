import pandas as pd
import numpy as np

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