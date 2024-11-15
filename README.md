# History’s Plot Twist: Cinematic genre, diversity, and popularity as the ultimate mirror 

## Abstract  
In the world of cinema, movies often do more than entertain—they capture and reflect the 
societal pulse of their time. This project seeks to understand how genre complexity and cast 
diversity in films can serve as mirrors of global events and cultural shifts through ratings. By 
analyzing data from CMU, IMDb, and Wikidata sources, we examine how diverse 
demographic representations and complex genre combinations influence ratings and reveal 
trends that resonate with audiences across different eras and regions. This research is 
motivated by the want to fulfill our beliefs that region and time impact population’s 
perceptions of the media they consume. By viewing films through this lens, filmmakers, 
critics, and enthusiasts alike can better understand cinema’s role as both a reflection and an 
influencer of the world’s shifting social and cultural landscape.

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

## Proposed timeline 
- Week 1: Review steps 1-5 + Homework 2 
- Week 2: Repeat steps 5-7 across genres, region, and/or time periods 
- Week 3: Step 8 + 9 
- Week 4: Step 10 + 11 
- Week 5: Compile final data story, clean repository, and finalize interactive webpage. 

## Organization within the team:  
Despite the below divisions, we work collaboratively and continuously to ensure we remain up 
to date on the project happenings and to ensure no one's thinking becomes too pigeonholed. 
- Week 1: All 
- Week 2: Jake and Alexis 
- Week 3: Mariem, Jacopo, Chiara 
- Week 4: Jake, Jacopo, Chiara, Mariem 
- Week 5: All  

## Questions for TAs:  
We’ll be in contact with Ziyi. 

## References 
[1] Asaniczka, and themoviedb.org. (2024). Full TMDB Movies Dataset 2024 (1M Movies)  
[Data set]. Kaggle. https://doi.org/10.34740/KAGGLE/DSV/9904037 

[2] Movielens. (2019). MovieLens 25M Dataset [Data set]. Grouplens.  
https://files.grouplens.org/datasets/movielens/ml-25m-README.html  

[3] https://query.wikidata.org/ 


### Datasets
To get the datasets for the analysis, download from http://www.cs.cmu.edu/~ark/personas/ and https://www.kaggle.gicom/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies. 



## Project Structure

The directory structure of new project looks like this:

```
├── data                        <- Project data files
│
├── src                         <- Source code
│   ├── data                            <- Data directory
│   ├── models                          <- Model directory
│   ├── utils                           <- Utility directory
│   ├── scripts                         <- Shell scripts
│
├── tests                       <- Tests of any kind
│
├── results.ipynb               <- a well-structured notebook showing the results
│
├── .gitignore                  <- List of files ignored by git
├── pip_requirements.txt        <- File for installing python dependencies
└── README.md
```

