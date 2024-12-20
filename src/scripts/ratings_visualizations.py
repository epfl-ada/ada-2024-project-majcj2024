import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import pmdarima as pm
from sklearn.metrics import mean_squared_error, r2_score

def plot_region_genre_ratings(mean_ratings, confidence_intervals, decades, top_20_genres_list, colors):
    """
    plot_region_genre_ratings - creates subplots showing the mean ratings of top 20 genres per region over six decades.

    Inputs: - mean_ratings (dict): a dictionary where each region maps to a 2D array of genre mean ratings per decade
            - confidence_intervals (dict): a dictionary where each region maps to a 2D array of genre confidence intervals per decade
            - decades (list): list of decades
            - top_20_genres_list (list): list of the top 20 genres
            - colors (list): list of colors for the plot, one per genre

    Outputs: - displays the plot for mean ratings and confidence intervals of genres over decades per region
    """
    # defining the subplots, with one per region
    fig, axes = plt.subplots(3, 3, figsize=(15, 15), sharey=True)
    axes = axes.flatten()

    # creating the subplot per region of their mean ratings for the top 20 genres of films over the six decades considered
    for i, region_name in enumerate(mean_ratings.keys()):
        ax = axes[i]

        # each genre will be stored as a row in the mean and confidence interval dictionaries
        # pairing and plotting their mean ratings and CI per decade
        for j, (mean, stderr) in enumerate(zip(mean_ratings[region_name], confidence_intervals[region_name])):

            # filtering datapoints with 0.0 mean
            mask = np.array(mean) != 0
            filtered_means = np.array(mean)[mask]
            filtered_stderrs = np.array(stderr)[mask]

            # applying mask to the decades to ensure correct matching
            filtered_decades = np.array(decades)[mask]

            # mapping the decades to integers
            decade_map = {i: int(i) for i in decades}
            filtered_decades_as_int = [decade_map[i] for i in filtered_decades]

            # sorting the decades in chronological order
            sorted_indices = np.argsort(filtered_decades_as_int)
            filtered_decades = np.array(filtered_decades_as_int)[sorted_indices]
            filtered_means = filtered_means[sorted_indices]
            filtered_stderrs = filtered_stderrs[sorted_indices]

            # plotting the genre mean ratings over decades with error bars
            color = colors[j]
            ax.errorbar(filtered_decades, filtered_means, yerr=filtered_stderrs, label=top_20_genres_list[j],
                        capsize=5, marker='o', color=color)
            ax.plot(filtered_decades, filtered_means, marker='o', color=color)

        ax.set_title(region_name)
        ax.set_xlabel('Decade')
        ax.set_ylabel('Mean Rating')

    plt.tight_layout()
    fig.legend(labels=top_20_genres_list, loc='lower center', ncol=5, bbox_to_anchor=(0.5, -0.05), fontsize='small')
    plt.show()

def plot_genre_region_mean_ratings(mean_ratings, confidence_intervals, regions, decades, colors, grid_shape=(2, 3)):
    """
    plot_genre_region_mean_ratings - plots the mean ratings and confidence intervals for different genres across regions and decades.
    
    Inputs: - mean_ratings (dict): dictionary containing mean ratings for each genre by region and decade
            - confidence_intervals (dict): dictionary containing the confidence intervals for each genre by region and decade
            - regions (list): list of region names
            - decades (list): list of decades
            - colors (list): list of colors for plotting each region's data
            - grid_shape (tuple): tuple specifying the grid shape for the subplots
        
    Outputs: - displays a plot displaying the mean ratings and confidence intervals for each genre across regions and decades
    """
    
    # defining the subplots with the given grid shape
    if grid_shape[0] == 2 and grid_shape[1] == 3:
        fig, axes = plt.subplots(grid_shape[0], grid_shape[1], figsize=(15, 8), sharey=True)
    else:
        fig, axes = plt.subplots(grid_shape[0], grid_shape[1], figsize=(15, 15), sharey=True)
        
    axes = axes.flatten()

    # creating the subplot per genre of their mean ratings for the regions over the six decades considered
    for i, genre_name in enumerate(mean_ratings.keys()):
        ax = axes[i]

        # each region is stored as a row in the mean and confidence interval dictionaries and 
        # must have their mean ratings and CI per decade paired and plotted
        for j, (mean, stderr) in enumerate(zip(mean_ratings[genre_name], confidence_intervals[genre_name])):

            # filtering datapoints with 0.0 mean
            mask = np.array(mean) != 0
            filtered_means = np.array(mean)[mask]
            filtered_stderrs = np.array(stderr)[mask]

            # applying mask to the decades to ensure correct matching
            filtered_decades = np.array(decades)[mask]

            # converting to numerical values
            decade_map = {i: int(i) for i in decades}
            filtered_decades_as_int = [decade_map[i] for i in filtered_decades]

            # sorting decades of a region with a mean rating reported
            sorted_indices = np.argsort(filtered_decades_as_int)

            # sorting the decades, means, and confidence intervals based on the sorted indices
            filtered_decades = np.array(filtered_decades_as_int)[sorted_indices]
            filtered_means = filtered_means[sorted_indices]
            filtered_stderrs = filtered_stderrs[sorted_indices]
            
            # defining the given genres color
            color = colors[j]
            ax.errorbar(filtered_decades, filtered_means, yerr=filtered_stderrs, label=regions[j], capsize=5, marker='o', color=color)
            ax.plot(filtered_decades, filtered_means, marker='o', color=color)

        ax.set_title(genre_name)
        ax.set_xlabel('Decade')
        ax.set_ylabel('Mean Rating')

    plt.tight_layout()
    fig.legend(labels=regions, loc='lower center', ncol=len(regions)//2, bbox_to_anchor=(0.5, -0.05), fontsize='small')
    plt.show()

def plot_top_worst_genres(top_worst_df, regions, decade_labels, decade_pairs, figsize=(14, 8)):
    """
    plot_top_worst_genres - creates a grid plot visualizing the top and worst-performing genres 
    across regions and consecutive decade pairs.

    Inputs: - top_worst_df (DataFrame): DataFrame containing columns 'region', 'decade1', 'decade2', 
                                        'top_genre', 'top_slope', 'worst_genre', 'worst_slope'
            - regions (list): List of unique regions
            - decade_labels (list): List of decade labels for the x-axis
            - decade_pairs (list): List of consecutive decade pairs
            - figsize (tuple, optional): Size of the plot

    Outputs: - plot of the data grid
    """
    # creating the figure for the plot
    fig, ax = plt.subplots(figsize=figsize)

    # setting axis limits and labels
    ax.set_xlim(0, len(decade_labels))
    ax.set_ylim(0, len(regions))
    ax.set_xticks(range(len(decade_labels)))
    ax.set_yticks(range(len(regions)))
    ax.set_xticklabels(decade_labels, fontsize=10)
    ax.set_yticklabels(regions, fontsize=10)
    ax.grid(visible=True, which='major', linestyle='-', linewidth=0.5)

    # defining colors
    top_color = sns.color_palette("Greens", n_colors=3)[2]  # Dark green
    worst_color = sns.color_palette("Reds", n_colors=3)[2]  # Dark red

    # looping through the grid
    for i, region in enumerate(regions):
        for j, (decade1, decade2) in enumerate(decade_pairs):
            # getting data for current cell
            cell_data = top_worst_df[
                (top_worst_df['decade1'] == decade1) & 
                (top_worst_df['decade2'] == decade2) & 
                (top_worst_df['region'] == region)
            ]

            if not cell_data.empty:
                top_genre = cell_data['top_genre'].values[0]
                top_slope = cell_data['top_slope'].values[0]
                worst_genre = cell_data['worst_genre'].values[0]
                worst_slope = cell_data['worst_slope'].values[0]
                
                # positioning text
                x_center, y_center = j + 0.5, i + 0.5
                
                # drawing background square
                ax.add_patch(patches.Rectangle((j, i), 1, 1, color="white", ec="black", lw=0.5))
                
                # adding top genre
                ax.text(x_center, y_center + 0.15, f"{top_genre} ({top_slope:.4f})", 
                        ha='center', va='center', fontsize=8, color=top_color, fontweight='bold')
                
                # adding worst genre
                ax.text(x_center, y_center - 0.15, f"{worst_genre} ({worst_slope:.4f})", 
                        ha='center', va='center', fontsize=8, color=worst_color, fontweight='normal')

    # legend
    handles = [
        patches.Patch(color=top_color, label="Top Genre"),
        patches.Patch(color=worst_color, label="Worst Genre")
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=2, fontsize=10)

    # titles and labels
    plt.title("Top and Worst Performing Genres by Region and Consecutive Decades", fontsize=14, fontweight='bold')
    plt.xlabel("Decade Pairs", fontsize=12)
    plt.ylabel("Regions", fontsize=12)

    plt.tight_layout()
    plt.show()

def calculate_and_plot_overall_means(df, regions, figsize=(15, 15)):
    """
    calculate_and_plot_overall_means - calculates overall mean ratings for each region and plots them.

    Inputs: - df (DataFrame): DataFrame containing columns 'region', '5yearbin', and 'averageRating'
            - regions (list): list of region names to analyze
            - figsize (tuple): size of the subplot grid (default: (15, 15))

    Outputs: - overall_means (dict): dictionary where keys are region names and values are Series of overall 
                                     mean ratings indexed by 5-year bins
             - displays a grid plot showing overall mean ratings for each region
    """
    overall_means = {}

    # calculating the average mean rating per 5-year bin for each region
    for region in regions:
        region_df = df[df["region"] == region]
        
        # calculating mean rating per 5-year bin
        genre_mean_ratings = region_df.groupby("5yearbin")["averageRating"].mean()
        
        # storing the result for this region
        overall_means[region] = genre_mean_ratings

    # plotting the overall mean ratings for each region
    fig, axes = plt.subplots(3, 3, figsize=figsize, sharey=True)
    axes = axes.flatten()

    for i, (region_name, overall_mean) in enumerate(overall_means.items()):
        ax = axes[i]
        x = overall_mean.index
        y = overall_mean.values
        ax.plot(x, y, marker='o', color='blue', label="Overall Mean")
        
        ax.set_title(region_name)
        ax.set_xlabel("5-Year Bin")
        ax.set_ylabel("Mean Rating")
        ax.legend()

    plt.tight_layout()
    plt.show()
    
    return overall_means

def fit_autoarima_models(overall_means, figsize=(15, 15)):
    """
    fit_autoarima_models - Fits AutoARIMA models for each region's time series data, 
    evaluates their performance, and visualizes the results.

    Inputs: - overall_means (dict): dictionary where keys are region names and values are DataFrames 
                                    containing time series data with time index and mean ratings
            - figsize (tuple): size of the subplot grid

    Outputs: - fitted_models (dict): dictionary of fitted AutoARIMA models for each region
             - forecast_results (dict): dictionary of in-sample fitted values for each region
             - error_metrics (dict): dictionary containing RMSE and R² metrics for each region
             - displays a grid plot showing actual vs fitted values for all regions
    """
    fitted_models = {}
    forecast_results = {}
    error_metrics = {}

    # initializing the subplot grid
    fig, axes = plt.subplots(3, 3, figsize=figsize, sharey=True)
    axes = axes.flatten()

    # autoARIMA model and plot for each region
    for i, (region, overall_mean) in enumerate(overall_means.items()):
        print(f"--- Fitting AutoARIMA for Region: {region} ---")
        
        # dropping nans and resetting index
        overall_mean = overall_mean.dropna().reset_index()
        time_series = overall_mean.iloc[:, 1]
        time_index = overall_mean.iloc[:, 0]
        
        # fitting AutoARIMA model
        try:
            model = pm.auto_arima(
                time_series, seasonal=False, stepwise=True, 
                trace=False, suppress_warnings=True
            )
            print(f"Best Model for {region}: {model}")
            
            # forecasting in-sample fitted values
            fitted_values = model.predict_in_sample()
            
            # calculating error metrics
            rmse = np.sqrt(mean_squared_error(time_series, fitted_values))
            r2 = r2_score(time_series, fitted_values)
            
            # storing the fitted model, results, and metrics
            fitted_models[region] = model
            forecast_results[region] = fitted_values
            error_metrics[region] = {'RMSE': rmse, 'R²': r2}
            
            # plotting actual vs fitted values
            ax = axes[i]
            ax.plot(time_index, time_series, label="Actual Data", marker='o', color="blue")
            ax.plot(time_index, fitted_values, label="Fitted AutoARIMA", marker='o', color="red")
            ax.set_title(region)
            ax.set_xlabel("5-Year Bin")
            ax.set_ylabel("Mean Rating")
            ax.legend()
            ax.tick_params(axis='x', rotation=45)
            
        except Exception as e:
            print(f"Error fitting AutoARIMA for region {region}: {e}")
            continue

    plt.tight_layout()
    plt.show()

    # printing error metrics
    for region, metrics in error_metrics.items():
        print(f"Region: {region} --> RMSE: {metrics['RMSE']:.4f}, R²: {metrics['R²']:.4f}")
    
    return fitted_models, forecast_results, error_metrics

def forecast_regions(fitted_models, overall_means, forecast_horizon=4, 
                              selected_regions=["India", "North America", "Western Europe"]):
    """
    forecast_regions - forecasts future mean ratings for selected regions using 
    fitted AutoARIMA models and visualizes the actual data and forecasted values

    Inputs: - fitted_models (dict): dictionary of fitted AutoARIMA models for each region
            - overall_means (dict): dictionary where keys are region names and values are Series of 
                                overall mean ratings indexed by 5-year bins
            - forecast_horizon (int, optional): number of time steps to forecast (default: 4)
            - selected_regions (list, optional): list of region names to forecast for 

    Outputs: - future_predictions (dict): dictionary where keys are region names and values are the 
                                      forecasted values for the next time steps
             - displays a grid plot showing the actual data and forecasted values for each selected region
    """
    future_predictions = {}
    fig, axes = plt.subplots(1, len(selected_regions), figsize=(18, 6))
    axes = axes.flatten()

    for i, region in enumerate(selected_regions):
        print(f"--- Forecasting for Region: {region} ---")
        
        # getting the fitted model and its original data
        model = fitted_models[region]
        overall_mean = overall_means[region].dropna().reset_index()
        time_series = overall_mean.iloc[:, 1]
        time_index = overall_mean.iloc[:, 0]
        
        # forecasting future values
        future_forecast = model.predict(n_periods=forecast_horizon)
        future_predictions[region] = future_forecast
        
        # extending the time index for the forecast
        future_time_index = list(range(len(time_index), len(time_index) + forecast_horizon))
        
        # plotting the actual data and forecast
        ax = axes[i]
        ax.plot(time_index, time_series, label="Actual Data", marker='o', color="blue")
        ax.plot(future_time_index, future_forecast, label="Forecast (20 years)", marker='o', color="green")
        ax.set_title(region)
        ax.set_xlabel("5-Year Bin (Extended)")
        ax.set_ylabel("Mean Rating")
        ax.legend()
        ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()
    
    return future_predictions