# Predicting NFL Matchup Results
This project aims to predict the results of NFL game matchups. Python will be implemented in the data collection, preprocessing, model selection and evaluation stages of the data science project lifecycle.

### Data Collection
All game summary statistics from 2003-2017 were scraped from [Pro Football Reference](https://www.pro-football-reference.com/) using the scrapy package, and the Elo ratings for each matchup were provided by [FiveThirtyEight](https://github.com/fivethirtyeight/nfl-elo-game). 

### Preprocessing
The moving average differential team metrics and basic game day information prior to each game will be used as features for each prediction. The metrics were calculated by:
1.	Generating 2003-2017 season average statistics for each team 
2.	Initiating each team’s week 1 stats using the previous season’s average

### Predictive Analysis
Walk forward cross-validation was performed for tuning and model selection. The following algorithms were used to generate candidate models:
1.	Logistic Regression
2.	Random Forest
3.	Artificial Neural Networks
4.	Gradient Boosting

### Final Results
The Gradient Boosted Trees model was selected to evaluate the test set. The final model yielded a predictive accuracy of 72.3% for the 2017 season compared to the baseline performance of 70.3%.

### Project Files
The project contains the following:
1.	NFLScraper – Folder containing all the web scraping scripts
2.	Data – Folder containing scraped data and Elo ratings from FiveThirtyEight's [repository](https://github.com/fivethirtyeight/nfl-elo-game)
3.	preprocess.py – Python script used to prepare the data
4.	analysis.py – Python script used for modeling and scoring
5.	nfl_cleaned.csv – The dataset returned after preprocessing
