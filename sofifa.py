## Import packages
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import time
import pandas as pd

## Define functions
def scrape_players(soup, update):
    """
    For a single page on sofifa.com, scrape every player's info into a list [name, short_name, rating, team, id, update, update_date], and append all players to a list.
    """
    players = soup.find_all("tr", class_="")
    players_list=[]
    for player in players:
        name = player.find("a")["data-tippy-content"]
        short_name = player.find("a").text
        rating = int(player.find("em").text)
        # Find the next chunk of html after <figure> with class "avatar small transparent", since the team is always after this code
        team_sibling = player.find("figure", class_="avatar small transparent").find_next_sibling()
        team = team_sibling.text
        id = player.find("img")["id"]
        # Find the date of the current update
        update_date = soup.find("select", {"name": "roster"}).select_one('option[selected]').text
        new_player = [name, short_name, rating, team, id, update, update_date]
        players_list.append(new_player)
    return players_list

def set_new_soup(new_url):
    """
    Overwrites soup for new url.
    """
    global url, request, response, html, soup
    url = new_url
    request = Request(url, headers = header)
    response = urlopen(request, timeout=10)
    html = response.read().decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')

def get_next_url(soup):
    """
    Gets the url to the next page to scrape. Returns None if there is no next page.
    """
    for button in soup.find_all("a", class_="button"):
        if "Next " in button.text:
            new_url = "https://sofifa.com" + button["href"]
            return new_url
    # return None if no "Next" button was found after iterating through all the buttons
    return None

def scrape_update(update):
    """
    Scrapes all pages of players for a single update on sofifa.com, as well as the update date (function scrape_date).
    """
    # Setup BeautifulSoup
    global url, header, request, response, html, soup
    url = "https://sofifa.com/players?type=all&lg%5B0%5D=13&r=" + str(update) + "&set=true&offset=0"
    header = {'User-Agent': 'Mozilla/5.0', "accept-language": "en-US"}
    request = Request(url, headers = header)
    response = urlopen(request, timeout=10)
    html = response.read().decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    
    all_players = []
    # While there is still a "Next" page button, we scrape players on the page.
    while get_next_url(soup) is not None:
        page_players = scrape_players(soup, update)
        all_players.append(page_players)
        new_url = get_next_url(soup)
        set_new_soup(new_url)
    # After exiting the loop, we still need to scrape the players on the last page.
    page_players = scrape_players(soup, update)
    all_players.append(page_players)
    
    return all_players

def scrape_game(first_update, last_update):
    """
    Scrapes range of updates in a EA FIFA game.
    """
    game_players = []
    errors = []
    # Record start time
    start_time = time.time()

    # Iterate over every update and scrape_update(update)
    for update in range(first_update, last_update + 1):
        try:
            update_players = scrape_update(update)
            game_players.append(update_players)
            print("\rUpdate {}/{} scraped".format((update - first_update + 1), (last_update + 1 - first_update)), end='', flush=True)
        # Catch errors and append to errors list with the corresponding update
        except Exception as e:
            errors.append((update, e))
    
    # Record end time and elapsed time to scrape game.
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print("\nScraping all updates took {} minutes and {} seconds".format(minutes, seconds))

    # Print updates that returned errors
    if errors:
        print("Errors occurred while scraping the following updates:")
        for update, error in errors:
            print("Update {}: {}\n".format(update, error))
            
    return game_players

# We can't directly turn this into a dataframe like for Premier League, because the dimensions of the nested list are uneven. We will flatten the list 3 times first.
def flatten_list(nested_list):
    flat_list = []
    flat_list_2 = []
    flat_list_3 = []
    for list in nested_list:
        flat_list.extend(list)
    for list in flat_list:
        flat_list_2.extend(list)
    for list in flat_list_2:
        flat_list_3.extend(list)
    return flat_list_3

## Execute functions
# Ask user for numbers of games and updates

# Maximum tries for while loops
max_tries = 2

print("Sofifa.com player scraper\n")
tries = 0
while tries <= max_tries:
    try:
        print("How many games to scrape?")
        num_games = int(input())
        # Break out of the loop if input is successfully converted to an integer
        break  
        # Return error if input is not an integer.
    except ValueError:
        if tries == max_tries:
            print("Maximum number of attempts reached. Exiting program.")
            exit()
        print("Invalid input. Please enter an integer.")
        tries += 1

first_updates = []
last_updates = []

# Get updates from user
for i in range(1, num_games + 1):
    tries = 0
    while tries <= max_tries:
        try:
            print("First update in game {}:".format(i))
            first_update = int(input())
            # Break out of the loop if input is successfully converted to an integer
            break  
            # Return error if input is not an integer.
        except ValueError:
            if tries == max_tries:
                print("Maximum number of attempts reached. Exiting program.")
                exit()
            print("Invalid input. Please enter an integer.")
            tries += 1

    first_updates.append(first_update)

    tries = 0
    while tries <= max_tries:
        try:
            print("Last update in game {}:".format(i))
            last_update = int(input())
            # Break out of the loop if input is successfully converted to an integer
            break  
            # Return error if input is not an integer.
        except ValueError:
            if tries == max_tries:
                print("Maximum number of attempts reached. Exiting program.")
                exit()
            print("Invalid input. Please enter an integer.")
            tries += 1

    last_updates.append(last_update)

games_list = []

# Append all games to one list
print("\nScraping beginning...")
for i in range(len(first_updates)):
    scraped_game = scrape_game(first_updates[i], last_updates[i])
    games_list.append(scraped_game)
    
# Flatten games list
games_list = flatten_list(games_list)
print("\nAll players from all games scraped.")

# Convert list to pandas dataframe
print("Input desired file/dataframe name:")
file_name = input()
df_name = file_name + "_df"
locals()[df_name] = pd.DataFrame(games_list, columns=["name", "short_name", "rating", "team", "id", "update", "update_date"])
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