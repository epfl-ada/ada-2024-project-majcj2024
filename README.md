# Rating Detectives: Modeling Movie Ratings with Multidimensional Features 🔍

## Abstract  
Movies offer more than entertainment as they are reflections of societal trends and cultural shifts. This project investigates the key features influencing movie ratings, focusing on attributes like release date, country of production, and innovative metrics such as historical proximity scores and Shannon Diversity Indices for ethnicity and gender. We demonstrate that ratings vary significantly across regions and genres, supported by ANOVA and Kruskal-Wallis tests, with notable exceptions being that documentaries and romantic comedies fail to disprove ratings across regions in these genres vary to a statistically significant degree. Temporal trends also reveal significant variations in ratings, though release date alone proves insufficient as a predictive feature, leading to the development of enhanced attributes for analysis. Using a Random Forest model that ensembles 100 individual decision trees, our trained model on a 80-20 data split and cross-validated with 10 folds achieves a mean training score of 75.26%, which corresponds to an accuracy of 76.8% on previously unseen data. From our developed model, we identify the importance of features on predicting movie ratings. Release date is identified as the most influential predictor, with a Gini Importance score of 0.2456. This model captures the dynamic evolution of movie ratings and offers a reliable framework for analyzing unlabelled films, providing valuable insights into how genre, region, and time shape audience perceptions.

[Find our datastory here](https://doalexis.github.io/majcj2024/)

## Research Questions:  
- How do film ratings vary across regions and genres, and how has this evolved over time?
- What is the influence of cast demographics, including ethnicity and gender, on ratings? 
- How have traditional genres blended into complex combinations of genres assigned to movies, and is this a relevant feature for predicting a movies average rating?
- Can we create a score to identify movies that are proximal in release date to significant regional cultural moments, and this score's impact on ratings?
- What novel features can be prepared to predict movie ratings based on available characters metadata? 
- How accurately can we prepare a classification model to label the ratings of unlabelled movies using features identified as being correlated with movie ratings?
- What feature is the most informative in assigning a rating out of 10 to a given movie?

## Employed additional datasets: 
Three additional datasets were used for constructing our datastory.  
1. Full TMDB Movies Dataset 2024 (1M Movies) [1]: This dataset includes metadata (e.g. revenue, runtime, release date, and IMDB ID) to complement the CMU dataset. This “.csv” downloadable dataset contains about 1.4M movie’s metadata, yet only 100K entries remain upon merging to the CMU Corpus.
2. IMDb Non-Commercial Dataset [2]: This ".tsv" dataset from IMDb contains movie average ratings on a scale of 10. Each movies rating is an average value calculated by IMDb in an undisclosed way, as an effort to prevent user bias when rating movies.
3. Wikidata Dataset [3]: A supplementary, manually generated dataset from Wikidata containing the freebase IDs, nationalities and missing ethnicities of the actors in our original movie Corpus.

## Methods 
### Part 1: Data enrichment and cleaning 
**Step 1 - Loading and cleaning movie metadata**: Movie metadata was loaded from the CMU Corpus and stripped of duplicate movie entries, retaining only unique titles, which accounted for about 5% of the data. Movies with missing release dates were excluded, and date formats were standardized to facilitate merging.

**Step 2 - Enriching movies and characters datasets**: Ratings data from IMDb were linked to the TMDB dataset using IMDb IDs. This rating-enriched TMDB dataset was merged with the movies dataset using a  unique index of movie titles and release dates. This resulted in a dataset of 32,972 unique films with enriched metadata for analysis. These movies were then grouped into nine geographical regions: North America, Central and South America, Western Europe, Eastern Europe, South Africa and Central Africa, North Africa and Middle East, India, Remaining Asia, and Oceania. The characters dataframe was also enriched using the freebaseIDs of actors lacking ethnicity information to retrieve their ethnicities and nationality information, by quering wikidata and importing these results in a ".csv" file to merge to the characters dataset.

**Step 3 - Handling multiple genres and countries**: Movies with multiple countries were removed from the enriched dataset to ensure independency of ratings across geographies. Movies with multiple genres were exploded into separate entries to retrieve the top 20 singular genres for analysis: action, action/adventure, adventure, black-and-white, comedy, crime fiction, documentary, drama, family, horror, indie, musical, mystery, romance, romantic comedy, romantic drama. short, silent, thriller, world cinema. All future analyses were therefore on ratings over these 20 major genres and 9 regions.

### Part 2: General analysis 
**Step 4 - Production frequency distributions**: The normality of movie average ratings was confirmed with a Q-Q plot. The distributions of production frequencies across genres as well as average ratings binned into 0.5 increments across the top 20 geanres were also analyzed using histograms and heatmaps, respectively. This revealed genre-specific distributions, with documentaries scoring highest versus horror films skewed towards lower ratings.

**Step 5 - Understanding associations of movie metadata and ratings**: Quantitative movie metadata features (ie. runtime, revenue, and ratings) were combinatorially explored for their correlations via visual interpretation and using Pearson and Spearman coefficients. Runtime positively correlates with ratings (Pearson correlation: 0.1222, p-value < 0.0001; Spearman: 0.1767, p-value < 0.0001), whereas release date negatively correlated with ratings (Pearson: -0.1029, p-value < 0.0001; Spearman: -0.0858, p-value < 0.0001). These relationships, though statistically significant, were weak. This analysis was then re-performed per genre in our top 20 list, demonstrating the positive association between runtim and ratings is not upheld for world cinema and short films. Similarly, the association for release dates and ratings across genres revealed silent, black-and-white, indie, documentary, and short films have positive relationships, in contrast to the negative release date-rating association observed across all movies.

### Part 3: Ratings analyzed over genres, and production regions and decades
**Step 6 - Variation of ratings by region and genres**: Visual analysis of mean ratings across regions grouped by genres and then across genres grouped by regions were prepared as bar charts with 95% confidence intervals. ANOVA tests of these distributions reveal significant differences in average ratings by region when grouping movies by genres, except for documentary films (p-value = 0.457 > 0.05) and romantic comedies (p-value = 0.141 > 0.05). Conversely, grouping by genres and analyzing ratings over regions using Kruskal-Wallis tests showed significant differences in average ratings for most genres between regions except for (Kruskal-Wallis Statistic: 24.0638, p-value = 0.1937 > 0.05).

**Step 7 - Variation of ratings by region and genres, and time**: Visual analysis of mean ratings between regions grouped by genre over production decades and of mean ratings between genres grouped by regions over production decades were prepared as lineplots with 95% confidence intervals. An ANOVA test modelling the interaction of a movies genre and decade of release on average ratings revealed a significant interaction (p-value < 0.001) indicating that the dynamic of ratings over time is genre-specific. Further analysis of the lineplot slopes between decades identified that rating changes over time for movies of a given genre in one region are not consistently increasing or declining.

**Step 8 - Time series analysis of ratings**: Given average movie ratings differ greatly across time when grouped by genre and region of production, an autoregressive integrated moving average (ARIMA) attempted to model ratings over decades. The ARIMA-predicted average ratings of a given region's movies was not consistenet with the true data, indicating that further features for rating predictions are required.

### Part 4: Generating novel movie features
**Step 9 - Making sense of characters data**: To make sense of the characters dataset, the association between the number of actors and movie ratings showed a weak positive association (Pearson correlation: 0.0354, p-value: 0.0000 Spearman correlation: 0.0342, p-value: 0.0000). Each region's composition of actor ethnicities, distribution of in-region versus out-of-region actor ethnicities, and gender representation was visualized.

**Step 10 - Impact of complex genre and actor demographics on regional ratings**: We identified the need for a Shanon Diversity Index (SDI) to indicate a movie's inclusivity for actor ethnicities. Two SDI for actor ethnicities and genders were prepared. Grouping movies by SDI ethnicity in 0.5 increments revealed significant differences in mean ratings (ANOVA p-value: 0.0299), with a weak negative correlation between SDI ethnicity and ratings (Pearson: -0.0364, p-value = 0.0100; Spearman: -0.0430, p-value = 0.0024). Similarly, SDI gender showed a weak negative association with ratings (Pearson: -0.0403, p-value = 0.0044; Spearman: -0.0352, p-value = 0.0128). An ANOVA comparing movies with SDI gender values above and below 0.5 also showed significant rating differences (p-value: 0.0069).

**Step 11 - Historical proximity scoring and genre complexity**: Two final features for predicting movie ratings were prepared. Historical events considered across five categories, wars and conflicts, political transformations, economic events, social and cultural milestones, and international relations and treaties were mapped to regions and their years of occurance. This event generation was performed using ChatGPT 4o [4]. The genre complexities were appended to movies metadata based on their count of genres originally listed in our top 20 genre list.

### Part 5: Predicting movie ratings combining generated features: 
**Step 12 - Predictability of ratings**: A random forest model was called on the features release date, runtime, genre, budget, region, number of actors, SDI ethnicity, SDI gender, number of languages, historical proximity score, and genre count. An 80-20 train-test split with 10-fold scoring of the training data revealed a mean score of 0.7519 ± 0.00559. On the test data, the average rating target of movies was 0.768. 

**Step 13 - Assessing the most informative average rating classifier**: The Gini Importance scores of the 11 features used for our random forest model were plotted to identify movie release date as the most informative feature for average movie rating predictions.

### Part 6: Formatting the final datastory and expanding modular file organization
**Step 14 - Learning website creation**: We self-taught PlotLy, Jekyll, CSS, and JavaScript to prepare the final datastory.

## Executed timeline:
| **Week** | **Tasks**                                                                         |
|----------|-----------------------------------------------------------------------------------|
| Week 0   | Prepared steps 1-4 for P2                                                        |
| Week 1   | Reviewed P2 + Homework 2                                                         |
| Week 2   | Executed steps 5-8                                                               |
| Week 3   | Step 9-11                                                                        |
| Week 4   | Step 12-13                                                                       |
| Week 5   | Step 14, compiling the final data story, and cleaning the repository.            |


## Organization within the team:  
Despite the below divisions, we worked collaboratively throughout the term, meeting on a weekly basis over all 14-weeks, as to continuously ensure we remained up to date on the project happenings and to ensure no one's thinking became too pigeonholed. 
| **Week**   | **Participants**                        |
|------------|-----------------------------------------|
| Week 0     | All                                     |
| Week 1     | All                                     |
| Week 2     | Jake and Alexis                         |
| Week 3     | Mariem, Jacopo, Chiara                  |
| Week 4     | Jake, Jacopo, Chiara, Mariem            |
| Week 5     | Alexis for website, rest for datastory  |

## References 
[1] Asaniczka, and themoviedb.org. (2024). Full TMDB Movies Dataset 2024 (1M Movies)  
[Data set]. Kaggle. https://doi.org/10.34740/KAGGLE/DSV/9904037 

[2] IMDb. (2024). IMDb Non-Commercial Datasets [Data set]. IMDb.  
https://developer.imdb.com/non-commercial-datasets/

[3] https://query.wikidata.org/ 

[4] OpenAI. (2023). ChatGPT (Mar 14 version) [Large language model]. https://chat.openai.com/chat

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