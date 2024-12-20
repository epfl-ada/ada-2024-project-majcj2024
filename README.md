# Rating Detectives: Modeling Movie Ratings with Multidimensional Features 🔍

## Abstract  
Movies offer more than entertainment as they are reflections of societal trends and cultural shifts. This project investigates the key features influencing movie ratings, focusing on attributes like release date, country of production, and innovative metrics such as historical proximity scores and Shannon Diversity Indices for ethnicity and gender. We demonstrate that ratings vary significantly across regions and genres, supported by ANOVA and Kruskal-Wallis tests, with notable exceptions being that documentaries and romantic comedies fail to disprove ratings across regions in these genres vary to a statistically significant degree. Temporal trends also reveal significant variations in ratings, though release date alone proves insufficient as a predictive feature, leading to the development of enhanced attributes for analysis. Using a Random Forest model that ensembles 100 individual decision trees, trained on an 80-20 data split and cross-validated with 10 folds, our approach achieves a mean accuracy of 75.26% in predicting movie ratings. Feature importance analysis highlights release date as the most influential predictor, with a Gini Importance score of 0.2456. This model captures the dynamic evolution of movie ratings and offers a reliable framework for analyzing unlabelled films, providing valuable insights into how genre, region, and time shape audience perceptions.

[Find our datastory here](https://doalexis.github.io/majcj2024/)

## Research Questions:  
- How do film ratings vary across regions and genres, and how has this evolved over time?
- What is the influence of cast demographics – ethnicity and gender – on ratings, and do these effects differ by region? 
- How have traditional genres blended into complex combinations of genres assigned to movies?
- Can we identify time periods of historical or cultural events that coincide with significant rating shifts in movies?
- What novel features from characters metadata can be prepared to indicate movie diversity to contribute to movie rating predictions? 
- How accurate can we prepare a classification model to label the ratings of unlabelled movies?
- What feature is the most informative in assigning a rating out of 10, incremented by 0.5 to a movie that's rating is unknown?

## Employed additional datasets: 
Three additional datasets were used for constructing our datastory.  
1. Full TMDB Movies Dataset 2024 (1M Movies) [1]: This dataset includes metadata (e.g. revenue, runtime, release date, and IMDB ID) to complement the CMU dataset. This “.csv” downloadable dataset contains about 1.4M movie’s metadata, yet only 100K entries remain upon merging to the CMU Corpus.
2. IMDb Non-Commercial Datasets [2]: This ".tsv" dataset from IMDb contains movie average ratings on a scale of 10. Each movies rating is an average value calculated by IMDb in an undisclosed way, as an effort to prevent user bias when rating movies if the average rating equation were known publicly.
3. Wikidata Dataset [3]: A supplementary, manually generated dataset from Wikidata containing the freebase IDs, nationalities and missing ethnicities of the actors in our original movie Corpus.

## Methods 
### Part 1: Data enrichment and cleaning 
**Step 1 - Loading and cleaning movie metadata**: Movie metadata was loaded from the CMU Corpus and stripped of duplicate movie entries were dropped, retaining only unique titles, which accounted for about 5% of the data. Movies with missing release dates were excluded, and date formats were standardized to facilitate merging.

**Step 2 - Enriching movies and characters datasets**: Ratings data from IMDb were linked to the TMDB dataset using IMDb IDs. The TMDB dataset, which had duplicates based on IMDb IDs, was deduplicated and merged with the movies dataset using a  unique index of  movie titles and release dates. The characters dataframe was also enriched using the Wikidata dataset to add more ethnicity information.

**Step 3 - Handling genres and countries**: Movies with multiple countries were removed from the enriched dataset to ensure independency of ratings across geographies. Movies with multiple genres were exploded into separate entries to retrieve the top 20 singular genres for analysis. We then focussed all future analysis on major these 20 major genres.

**Step 4 - Character dataset enrichment**: The characters dataset was cleaned and enriched with additional attributes such as ethnicity, gender, and age. Missing values were handled using custom functions, ensuring data completeness. Actor demographic information was standardized and merged with other datasets for consistent analysis.



### Part 2: Distribution analysis 
**Step 4 - Understanding attribute distributions**: Quantitative movie metadata features (ie. runtime, 
revenue, and ratings) were analyzed for distribution patterns using methods like the Kolmogorov
Smirnov goodness-of-fit test. Features requiring normality were further corrected via Box-Cox 
transformation. 

### Part 3: Ratings causal inference 
**Step 5 - Variation of ratings by region**: A t-test was performed for mean ratings between North 
America and Europe and will be repeated across all regional combinations. Similarly, ANOVA analysis 
already performed across all movies per region will be used to compare mean ratings across all genres 
per region.  

**Step 6 - Causality of region and actor demographics on genre ratings**: Propensity scoring movies 
on actor demographic and genre dummy features for movie country will be used to determine causality 
of production country on genre ratings, as already performed between the US and the UK for thriller 
films based on visualization on t-tests. In order to quantify the ethnic diversity of casts, we calculated a 
simple proportion-based index, later enriched with Shannon entropy to capture the uniformity of 
representation. A similar approach will be used to study the gender distribution of actors and whether 
these features are causal on regional ratings. 

**Step 7 - Time series analysis of ratings**: To infer regional population sentiment shifts associated 
with historical events, stationarity and autocorrelation functions will be applied to determine p and q 
coefficients of an ARMA(p,q) model, as demonstrated for all movies in Africa. By clustering movies 
by subject and analyzing ratings over time (using timestamps instead of overall mean ratings), we will 
identify how sentiments change based on film content throughout historical periods. 

### Part 4: Genre sophistication 
**Step 8 - Genre combinations**: A line chart per unique genre combination over time will be 
prepared. Additionally, the distribution of unique complex genre combinations summed over 
the past century across all regions will be compared with a chi-squared test. 

**Step 9 - Impact of complex genre and actor demographics on regional ratings**: Step 6’s 
causality tests will be repeated with complex genres, to determine if unique combinations of 
standard genres and their associated actor demographics are causal on ratings, per region.  

### Part 5: Predicting successful genre and demographic combinations: 
**Step 10 - Supervised learning via linear regression**: Based on prior causality analyses, linear 
regression will be prepared for regional ratings over genre and actor demographic features of 
importance. Unique genre combinations and actor demographics will be forecasted to indicate 
those most successful in each region’s future. 

**Step 11 - Predictability of ratings**: F-scores determined in cross-validating each model will 
be used to identify the region that’s predicted most successful genre and actor combination is 
most predictable. 

### Part 6: Formatting the final datastory and expanding modular file organization 

## Executed timeline:
| **Week** | **Tasks**                                                                         |
|----------|-----------------------------------------------------------------------------------|
| Week 1   | Reviewed P2 + Homework 2                                                         |
| Week 2   | Repeat steps 5-7 across genres, region, and/or time periods                      |
| Week 3   | Step 8 + 9                                                                       |
| Week 4   | Step 10 + 11                                                                     |
| Week 5   | Compile final data story, clean repository, and finalize interactive webpage.    |


## Organization within the team:  
Despite the below divisions, we worked collaboratively throughout the term, meeting on a weekly basis over all 14-weeks, as to continuously ensure we remain up to date on the project happenings and to ensure no one's thinking becomes too pigeonholed. 
| **Week**   | **Participants**                        |
|------------|-----------------------------------------|
| Week 1     | All                                     |
| Week 2     | Jake and Alexis                         |
| Week 3     | Mariem, Jacopo, Chiara                  |
| Week 4     | Jake, Jacopo, Chiara, Mariem            |
| Week 5     | All                                     |

## References 
[1] Asaniczka, and themoviedb.org. (2024). Full TMDB Movies Dataset 2024 (1M Movies)  
[Data set]. Kaggle. https://doi.org/10.34740/KAGGLE/DSV/9904037 

[2] IMDb. (2024). IMDb Non-Commercial Datasets [Data set]. IMDb.  
https://developer.imdb.com/non-commercial-datasets/

[3] https://query.wikidata.org/ 

## Project Structure
The final directory structure of the project is the following:

```
├── data                        <- Project data files
│
├── src                         <- Source code
│   ├── data                            <- Data directory
│   ├── models                          <- Model directory
│   ├── utils                           <- Utility directory
│   ├── scripts                         <- Shell scripts
│    
├── results.ipynb               
│
├── .gitignore                  
├── pip_requirements.txt        
└── README.md
```

Note that in `data/` one should upload all required large datafiles (CMU datasets, [1], [2]).