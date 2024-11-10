import pandas as pd

def fill_iqr(df, col, t=1.5):
    """
    fill_iqr - replaces a dataframe column outliers with mean of non-outliers, 
    assuming normality and applying +/- threshold*IQR of quantiles method

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