import pandas as pd
import numpy as np

def shannon_entropy(proportions):
    """
    shannon_entropy - Computes the Shannon entropy (diversity index) 
    for a given set of proportions.

    Inputs: - proportions (list or pd.Series): Proportions of categories in a group, 
              representing their relative frequencies or probabilities.

    Outputs: - entropy (float): The Shannon entropy value, calculated as a measure 
                of diversity. Higher values indicate greater diversity.
    """
    return -np.sum(proportions * np.log(proportions))