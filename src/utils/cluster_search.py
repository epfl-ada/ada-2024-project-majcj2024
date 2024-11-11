def col_search(col, cluster):
    """
    col_search - search and counts words of a particular cluster in the column 
    of a dataframe.

    Inputs: - col (string): column of the dataframe where to perform the search
            - cluster (list of strings): considered words cluster
    
    Outputs:
    """
    return sum(1 for word in cluster if word in col)