# Import packages
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import pandas as pd

## Define functions
# Scrape names of teams playing in match
def scrape_teams(soup):
    """
    Scrape names of teams playing in match.
    """
    teams = []
    team_names = soup.find_all("span", class_="mc-summary__team-name u-hide-phablet")
    for i in range(len(team_names)):
        teams.append(team_names[i].text)
    return teams


# Scrape match score and return a list
def scrape_score(soup):
    """
    Scrapes full-time score of a match.
    """
    scores = []
    score = soup.find("div", class_="mc-summary__score js-mc-score").text
    scores.append(score[0])
    scores.append(score[-1])
    return scores
    

# Scrape halftime score and return a list
def scrape_ht_score(soup):
    """
    Scrapes half-time score of a match.
    """
    scores = []
    score = soup.find("span", class_="js-mc-half-time-score").text
    scores.append(score[0])
    scores.append(score[-1])
    return scores
    

# Scrape match date
def scrape_date(soup):
    """
    Scrapes date of a match.
    """
    date = soup.find("div", class_="mc-summary__info").text
    date = date.strip()
    return date


# Scrape team formations and return a list
def scrape_formations(soup):
    """
    Scrapes the teams' formations in a match.
    """
    team_formations = []
    formations = soup.find_all("strong", class_="matchTeamFormation")
    team_formations.append(formations[0].text)
    team_formations.append(formations[-1].text)
    return team_formations


# First we subset the soup the divs that contain the starting players for the home and away team, then we iterate along the players and extract their name, position and id.
def scrape_players(soup):
    """
    This functions scrapes all starting players for a match, along with their respective position and id.
    """
    home_div = soup.find("div", class_="teamList mcLineUpContainter homeLineup")
    home_substitute_header = home_div.find("h3", class_="substituteHeader home")
    home_div = home_substitute_header.find_previous_sibling()
    # All the home players' names, positions and ids are in these divs.
    home_links = home_div.find_all("a", href=True)
    
    away_div = soup.find("div", class_="teamList mcLineUpContainter awayLineup")
    away_substitute_header = away_div.find("h3", class_="substituteHeader")
    away_div = away_substitute_header.find_previous_sibling()
    # All the home players' names, positions and ids are in these divs.
    away_links = away_div.find_all("a", href=True)

    players_list = []
    for player in home_links + away_links:
        name = player.find("div", class_="name").text.strip()
        position = player.find("span", class_="position").text.strip()
        id = player.get('href')
        # There are still some unwanted strings in the player attributes so we split and strip them.
        name = name.split("\n")[0].strip()
        position = position.split("\n")[-1].strip()
        id = id.split("/")[2]
        # Extract each player's attributes, and put them in a list.
        new_player = [name, position, id]
        # Append the list to a nested list of all players.
        players_list.append(new_player)

    return players_list


# Scrape all match information and return one list.
def scrape_all(soup):
    match = []
    match.append(scrape_teams(soup))
    match.append(scrape_score(soup))
    match.append(scrape_ht_score(soup))
    match.append(scrape_date(soup))
    match.append(scrape_formations(soup))
    match.append(scrape_players(soup))

    return match


# Iterate over Premier League urls for a season, each match has a unique url.
def scrape_season(first_match, last_match):
    """
    This function scrapes all match info for a range of PL matches.
    """
    season = []
    errors = []
    # Record start time
    start_time = time.time()
    
    # Iterate over every match in a season and append the scraped results to a list.
    for match in range(first_match, last_match + 1):
        try:
            # Setup BeautifulSoup
            global url, page, html, soup
            url = "https://www.premierleague.com/match/" + str(match)
            page = urlopen(url)
            html = page.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            match_data = scrape_all(soup)
            match_data.insert(0, match)
            season.append(match_data)
            print("\rMatch {}/{} scraped".format((match - first_match + 1), (last_match + 1 - first_match)), end='', flush=True)
        # Catch errors and append to errors list with the corresponding match
        except Exception as e:
            errors.append((match, e))
            
    # Record end time and elapsed time to scrape season.
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print("\nScraping all matches took {} minutes and {} seconds".format(minutes, seconds))

    # Print matches that returned errors
    if errors:
        print("\nErrors occurred while scraping the following matches:")
        for match, error in errors:
            print("Match {}: {}".format(match, error))

    return season

## Execute functions
# Ask user for numbers of seasons and matches

# Maximum tries for while loops
max_tries = 2

print("Premier League match scraper\n")
tries = 0
while tries <= max_tries:
    try:
        print("How many seasons to scrape?")
        num_seasons = int(input())
        # Break out of the loop if input is successfully converted to an integer
        break  
        # Return error if input is not an integer.
    except ValueError:
        if tries == max_tries:
            print("Maximum number of attempts reached. Exiting program.")
            exit()
        print("Invalid input. Please enter an integer.")
        tries += 1

first_matches = []
last_matches = []

# Get matches from user
for i in range(1, num_seasons + 1):
    tries = 0
    while tries <= max_tries:
        try:
            print("First match in season {}:".format(i))
            first_match = int(input())
            # Break out of the loop if input is successfully converted to an integer
            break  
            # Return error if input is not an integer.
        except ValueError:
            if tries == max_tries:
                print("Maximum number of attempts reached. Exiting program.")
                exit()
            print("Invalid input. Please enter an integer.")
            tries += 1

    first_matches.append(first_match)

    tries = 0
    while tries <= max_tries:
        try:
            print("Last match in season {}:".format(i))
            last_match = int(input())
            # Break out of the loop if input is successfully converted to an integer
            break  
            # Return error if input is not an integer.
        except ValueError:
            if tries == max_tries:
                print("Maximum number of attempts reached. Exiting program.")
                exit()
            print("Invalid input. Please enter an integer.")
            tries += 1

    last_matches.append(last_match)

seasons_list = []

# Append all seasons to one list
for i in range(len(first_matches)):
    scraped_season = scrape_season(first_matches[i], last_matches[i])
    seasons_list.append(scraped_season)
    
# Flatten seasons list
seasons_list = [item for sublist in seasons_list for item in sublist]
print("\nAll seasons scraped.")

# Convert list to pandas dataframe
print("Input desired file/dataframe name:")
file_name = input()
df_name = file_name + "_df"
locals()[df_name] = pd.DataFrame(seasons_list, columns=["match", "teams", "score", "ht_score", "date", "formations", "players"])
print("Dataframe saved as {}_df".format(file_name))

# Save dataframe as pickle
while True:
    print("Save as pickle? Y / N")
    # Convert input to lowercase
    save_as_pickle = input().lower()
    if save_as_pickle in ['y', 'yes']:
        locals()[df_name].to_pickle("{}.pkl".format(file_name))
        break
    elif save_as_pickle in ['n', 'no']:
        break
    else:
        print("Invalid input. Please enter 'Y' or 'N'.")

# Save dataframe as CSV
while True:
    print("Save as CSV? Y / N")
    # Convert input to lowercase
    save_as_csv = input().lower()
    if save_as_csv in ['y', 'yes']:
        locals()[df_name].to_csv("{}.csv".format(file_name), index=False)
        break
    elif save_as_csv in ['n', 'no']:
        break
    else:
        print("Invalid input. Please enter 'Y' or 'N'.")