# Rating Detectives: Modeling Movie Ratings with Multidimensional Features 🔍

## Abstract  
Movies are more than entertainment—they are reflections of societal trends and cultural shifts. This project investigates the key features influencing movie ratings, focusing on attributes like release date, country of production, and innovative metrics such as historical proximity scores and Shannon Diversity Indices for ethnicity and gender. We demonstrate that ratings vary significantly across regions and genres, supported by ANOVA and Kruskal-Wallis tests, with notable exceptions like documentaries and romantic comedies. Temporal trends also reveal significant variations in ratings, though release date alone proves insufficient as a predictive feature, leading to the development of enhanced attributes for analysis. Using a Random Forest model, trained on an 80-20 data split and cross-validated with 10 folds, our approach achieves a mean accuracy of 75.26% in predicting movie ratings. Feature importance analysis highlights release date as the most influential predictor, with a Gini Importance score of 0.2456. This model captures the dynamic evolution of movie ratings and offers a reliable framework for analyzing unlabelled films, providing valuable insights into how genre, region, and time shape audience perceptions.

## Research Questions:  
- How do film ratings vary across regions and genres, and how has this evolved over 
time? 
- What is the influence of cast demographics – ethnicity and gender – on ratings, and do 
these effects differ by region? 
- How have traditional genres blended into complex combinations, and how do regional 
preferences respond to these trends? 
- Can we identify time periods of historical or cultural events that coincide with 
significant rating shifts in movies, and for what cast demographics and cinematic 
subjects? 
- Can we predict which genre and demographic combinations will likely achieve the 
highest ratings in each region?  
- Which regions show the most consistent preferences in terms of genre and actor 
demographics? 

## Proposed additional datasets: 
Two additional datasets are to be used for constructing our datastory.  
1. Full TMDB Movies Dataset 2024 (1M Movies) [1]: This dataset includes metadata 
(e.g. revenue, runtime, release date, and IMDB ID) to complement the CMU dataset. 
This “.csv” downloadable dataset contains about 1.4M movie’s metadata, yet only 
100K entries remain upon merging to the CMU Corpus, which has not been too heavy 
so far. 
2. MovieLens 25M Movie Ratings [2]: This dataset from the University of Minnesota 
includes 25M movie ratings from MovieLens users chosen at random. Movie ratings 
include their IMDB IDs, allowing us to merge the ratings to the previously enriched 
CMU-TMDB dataset. Numerous ratings exist per movie, so the average rating per 
movie was calculated. 
3. Wikidata Dataset [3]: Supplementary dataset manually generated from Wikidata 
containing the freebase IDs, nationalities and missing ethnicities of the actors in our 
original database.

## Methods 
### Part 1: Data enrichment and cleaning 
**Step 1 - Enriching metadata**: Duplicate movie entries were retained only if they contained unique 
country attributes, ensuring data completeness. Missing attribute values in the CMU Corpus were filled 
using the TMDB’s entries, and movies without genres (about 1%) were dropped. The characters 
dataframe was also enriched using the Wikidata dataset to add more ethnicity information

**Step 2 - Handling several countries and genres**: Movies with multiple countries or genres were 
exploded into separate entries. To handle rare genres in exploded movies, we selected to keep only 
duplicate entries with genres amongst the top 90% of all genres.  

**Step 3 - Merging ratings**: MovieLens ratings were averaged per IMDB ID and linked to the CMU 
corpus using a provided linker file. Our final movies dataset includes 23,432 movies with ratings. 

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

## Proposed timeline:
| **Week** | **Tasks**                                                                         |
|----------|-----------------------------------------------------------------------------------|
| Week 1   | Review steps 1-5 + Homework 2                                                    |
| Week 2   | Repeat steps 5-7 across genres, region, and/or time periods                      |
| Week 3   | Step 8 + 9                                                                       |
| Week 4   | Step 10 + 11                                                                     |
| Week 5   | Compile final data story, clean repository, and finalize interactive webpage.    |


## Organization within the team:  
Despite the below divisions, we work collaboratively and continuously to ensure we remain up 
to date on the project happenings and to ensure no one's thinking becomes too pigeonholed. 
| **Week**   | **Participants**                        |
|------------|-----------------------------------------|
| Week 1     | All                                     |
| Week 2     | Jake and Alexis                         |
| Week 3     | Mariem, Jacopo, Chiara                  |
| Week 4     | Jake, Jacopo, Chiara, Mariem            |
| Week 5     | All                                     |

## Questions for TAs:  
We’ll be in contact with Ziyi. 

## References 
[1] Asaniczka, and themoviedb.org. (2024). Full TMDB Movies Dataset 2024 (1M Movies)  
[Data set]. Kaggle. https://doi.org/10.34740/KAGGLE/DSV/9904037 

[2] Movielens. (2019). MovieLens 25M Dataset [Data set]. Grouplens.  
https://files.grouplens.org/datasets/movielens/ml-25m-README.html  

[3] https://query.wikidata.org/ 

## Project Structure
The current directory structure of the project iss the following:

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
