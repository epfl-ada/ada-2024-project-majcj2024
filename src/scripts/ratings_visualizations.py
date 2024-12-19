import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_region_genre_ratings(mean_ratings, confidence_intervals, decades, top_20_genres_list, colors):
    """
    plot_region_genre_ratings - creates subplots showing the mean ratings of top 20 genres per region over six decades.

    Inputs: - mean_ratings (dict): a dictionary where each region maps to a 2D array of genre mean ratings per decade
            - confidence_intervals (dict): a dictionary where each region maps to a 2D array of genre confidence intervals per decade
            - decades (list): list of decades (e.g., [1950, 1960, 1970, 1980, 1990, 2000])
            - top_20_genres_list (list): list of the top 20 genres
            - colors (list): list of colors for the plot, one per genre

    Outputs: - Displays the plot for mean ratings and confidence intervals of genres over decades per region
    """
    # Defining the subplots, with one per region
    fig, axes = plt.subplots(3, 3, figsize=(15, 15), sharey=True)
    axes = axes.flatten()

    # Creating the subplot per region of their mean ratings for the top 20 genres of films over the six decades considered
    for i, region_name in enumerate(mean_ratings.keys()):
        ax = axes[i]

        # Each genre is stored as a row in the mean and confidence interval dictionaries
        # Pair and plot their mean ratings and CI per decade
        for j, (mean, stderr) in enumerate(zip(mean_ratings[region_name], confidence_intervals[region_name])):

            # Filter out datapoints with 0.0 mean (when under 3 movies were given)
            mask = np.array(mean) != 0
            filtered_means = np.array(mean)[mask]
            filtered_stderrs = np.array(stderr)[mask]

            # Apply the mask to the decades (x-values) to ensure correct matching
            filtered_decades = np.array(decades)[mask]

            # Map the decades to integers
            decade_map = {i: int(i) for i in decades}
            filtered_decades_as_int = [decade_map[i] for i in filtered_decades]

            # Sort the decades in chronological order
            sorted_indices = np.argsort(filtered_decades_as_int)
            filtered_decades = np.array(filtered_decades_as_int)[sorted_indices]
            filtered_means = filtered_means[sorted_indices]
            filtered_stderrs = filtered_stderrs[sorted_indices]

            # Plotting the genre mean ratings over decades with error bars
            color = colors[j]
            ax.errorbar(filtered_decades, filtered_means, yerr=filtered_stderrs, label=top_20_genres_list[j],
                        capsize=5, marker='o', color=color)
            ax.plot(filtered_decades, filtered_means, marker='o', color=color)

        ax.set_title(region_name)
        ax.set_xlabel('Decade')
        ax.set_ylabel('Mean Rating')

    # Adjust layout for readability
    plt.tight_layout()
    fig.legend(labels=top_20_genres_list, loc='lower center', ncol=5, bbox_to_anchor=(0.5, -0.05), fontsize='small')
    plt.show()

def plot_genre_region_mean_ratings(mean_ratings, confidence_intervals, regions, decades, colors, grid_shape=(2, 3)):
    """
    plot_genre_region_mean_ratings - Plots the mean ratings and confidence intervals for different genres across regions and decades.
    
    Inputs:
        - mean_ratings (dict): Dictionary containing mean ratings for each genre by region and decade
        - confidence_intervals (dict): Dictionary containing the confidence intervals for each genre by region and decade
        - regions (list): List of region names
        - decades (list): List of decades
        - colors (list): List of colors for plotting each region's data
        - grid_shape (tuple): Tuple specifying the grid shape for the subplots (default is (2, 3) for 2x3 subplots)
        
    Outputs:
        - A plot displaying the mean ratings and confidence intervals for each genre across regions and decades
    """
    
    # Defining the subplots with the given grid shape
    if grid_shape[0] == 2 and grid_shape[1] == 3:
        fig, axes = plt.subplots(grid_shape[0], grid_shape[1], figsize=(15, 8), sharey=True)
    else:
        fig, axes = plt.subplots(grid_shape[0], grid_shape[1], figsize=(15, 15), sharey=True)
        
    axes = axes.flatten()

    # Creating the subplot per genre of their mean ratings for the regions over the six decades considered
    for i, genre_name in enumerate(mean_ratings.keys()):
        ax = axes[i]

        # Each region is stored as a row in the mean and confidence interval dictionaries and must have their mean ratings and CI per decade paired and plotted
        for j, (mean, stderr) in enumerate(zip(mean_ratings[genre_name], confidence_intervals[genre_name])):

            # As some means were made to be 0.0 if under three movies were given for that genre in that decade per region, these datapoints must not be plotted
            mask = np.array(mean) != 0
            filtered_means = np.array(mean)[mask]
            filtered_stderrs = np.array(stderr)[mask]

            # The mask must be applied to the decades (x-values) over which the mean ratings are being plotted to ensure the correct rating is placed at the correct decade
            filtered_decades = np.array(decades)[mask]

            # The visualization of regional mean ratings over decades per genre requires numerical forms of the decade list previously made
            decade_map = {i: int(i) for i in decades}
            filtered_decades_as_int = [decade_map[i] for i in filtered_decades]

            # To ensure the subfigure's ratings are plotted chronologically, the decades of a region with a mean rating reported must be sorted
            sorted_indices = np.argsort(filtered_decades_as_int)

            # Sorting the decades, means, and confidence intervals based on the sorted indices
            filtered_decades = np.array(filtered_decades_as_int)[sorted_indices]
            filtered_means = filtered_means[sorted_indices]
            filtered_stderrs = filtered_stderrs[sorted_indices]
            
            # Defining the given genres color for plotting a line plot with error bars for every region's mean rating over the six decades in a given genre
            color = colors[j]
            ax.errorbar(filtered_decades, filtered_means, yerr=filtered_stderrs, label=regions[j], capsize=5, marker='o', color=color)
            ax.plot(filtered_decades, filtered_means, marker='o', color=color)

        ax.set_title(genre_name)
        ax.set_xlabel('Decade')
        ax.set_ylabel('Mean Rating')

    plt.tight_layout()
    fig.legend(labels=regions, loc='lower center', ncol=len(regions)//2, bbox_to_anchor=(0.5, -0.05), fontsize='small')
    plt.show()