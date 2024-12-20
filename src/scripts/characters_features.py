import numpy as np

def shannon_entropy(proportions):
    """
    shannon_entropy - computes the Shannon entropy (diversity index) 
    for a given set of proportions.

    Inputs: - proportions (list or pd.Series): proportions of categories in a group, 
              representing their relative frequencies or probabilities.

    Outputs: - entropy (float): Shannon entropy value, calculated as a measure 
                of diversity (higher values indicate greater diversity)
    """
    return -np.sum(proportions * np.log(proportions))