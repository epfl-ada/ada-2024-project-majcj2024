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

#def fill_cluster_col(df, col, col_q, dict):
    """
    fill_cluster_col - fills the column col of df based on
    the values in the query column col_q by choosing values of 
    a cluster (dict).

    Inputs: - df (dataframe): dataframe whose column needs to be filled
            - col (string): col to fill
            - col_q (string): query column
            - dict (dictionary): contains the clusters (and their names)
                                wrt which col will be filled
    
    Outputs:
    """
    # check if col does not exist (and fill with None if True)
#    if col not in df.columns:
#          df[col] = None

    # iterate on col nan entries
#    for index, row in df[df[col].isna()].iterrows():
        # expand the dictionary
#        for name, list in dict.items():
                # assing col value when the correct cluster is found
#                if row[col_q] in list:
#                        df.loc[index, col] = name
#                        break