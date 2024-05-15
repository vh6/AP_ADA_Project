# **AP_ADA_Project**
**Joint project for Advanced Programming and Advanced Data Analytics 2024**

**Data files:**
**CSV files E0 (1) through E0 (6)** are data with historical bookmaker odds for the past 6 seasons, downloaded from [football](https://www.football-data.co.uk/).
**all_seasons CSV and Pickle files** are the result of scraping with premierleague.py.
**all_games CSV and Pickle files** are the result of scraping with sofifa.py.
**matches_clean CSV and Pickle files**, as well as **id_df.pkl**, are the result of data wrangling with notebooks **id wrangling.ipynb** and **wrangling 2.ipynb**.
**test_100 and test_500 CSV and Pickle files** are subsets of matches_clean, that we simulate bets on in simulations.py.

**Python files:**
**premierleague.py** Used to scrape premierleague.com.
**sofifa.py** Used to scrape sofifa.com.

**Notebooks:**
**id wrangling.ipynb** Used to merge players from Premier League and Sofifa.
**wrangling 2.ipynb** Used to create features and labels for the neural network.
**neural network.ipynb** Used to create the machine learning model.
**simulations.py** Used to test the model.
