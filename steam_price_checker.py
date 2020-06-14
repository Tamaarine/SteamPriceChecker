# ------
# import statements
# ------
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import csv
import math
"""
Game, DLC type will have prices. Keep in mind there is also future games and free games that won't have price
Legacy media, Unknown, Demo, Tool will not have prices
"""

# Constants
max_display = 5
game_title = ""
app_type = ""
app_link = ""

# Link with inquiry
inquiry = 'https://steamdb.info/search/?a=app&q='

# Testing out csv first
csv_file = open('../../Downloads/data.csv', 'a')

csv_writer = csv.writer(csv_file)

csv_writer.writerow(['Game', 'Price', 'Date Updated'])


def display_price(app_id_link):

    link = 'https://steamdb.info' + app_id_link

    respond = Request(link, headers={'User-Agent': 'XYZ/3.0'})

    response = urlopen(respond, timeout=3).read()

    soup = BeautifulSoup(response, 'lxml')

    if app_type == "Demo":
        print()
        print("This app is a demo it doesn't have a price", "\n")

    elif app_type == "Legacy Media":
        print()
        print("This app is a legacy media it doesn't have a price", "\n")

    elif app_type == "Unknown":
        print()
        print("This app is unknown it doesn't have a price", "\n")

    elif app_type == "Tool":
        print()
        print("This app is a tool it doesn't have a price", "\n")
    else: # Either game, music, or dlc which we will show the price for

        try:

            price_table = soup.find('table', class_="table-prices")

            current_row = price_table.find('tr', class_="table-prices-current")

            tds = current_row.find_all('td')

            country = str(tds[0]["data-cc"]).upper() # Get the country + capitalize it
            price = str(tds[1].text)
            lowest_price = str(tds[3].text)

            if price == "N/A": # We were able to get the price but is free

                print()
                print("[", game_title, "is a free game", "]", "\n")

            else:

                # Printing of the price
                print()
                print("[", country, "-", game_title, "current price: ", price, "]")
                print("[", country, "-", game_title, " lowest price: ", lowest_price, "]")
                print()

        except Exception as e:

            generic_table = soup.find("table", "table table-bordered table-hover table-fixed table-responsive-flex")

            # Default to information tab so we can check the release state for information
            for tr in generic_table.find_all("tr"):
                if tr.td.text == "ReleaseState" and tr.find_all("td")[1].text == "prerelease":
                    print()
                    print("[", game_title, " is an upcoming title", "]", "\n")
                    break
                if tr.td.text == "ReleaseState" and tr.find_all("td")[1].text == "released":
                    print()
                    print("[", game_title, "is a free game", "]", "\n")
                    break


def handle_scrolling(results):

    # The items can be displayed in 5 or less items no need to scroll
    if len(results) <= max_display:

        for i in range(len(results)):
            print("[", i + 1, "]", results[i].find_all("td")[2].text, "\n")

    else:

        global lower_list
        global upper_list

        # Scrolling is required
        for i in range(lower_list, upper_list+1):
            print("[", i, "]", results[i-1].find_all("td")[2].text, "\n")


def search_games(given_game):

    global lower_list
    global upper_list
    global game_title
    global app_type
    global app_link
    # Function that performs the searching

    game_name = given_game.replace(" ", "+")  # Replace any spaces with percentage signs

    # Opening and getting the webpage source
    respond = Request(inquiry + game_name, headers={'User-Agent': 'XYZ/3.0'})
    response = urlopen(respond, timeout=5).read()

    # Putting it through beautifulsoup and getting the soup object
    soup = BeautifulSoup(response, 'lxml')

    # Finding the result table
    table = soup.find('table', class_="table-bordered")

    try:  # Next find the results in a try block

        actual_result = table.find_all('tr', class_="app")
        print()  # To clear up the space before

        # Working code right here
        total_item = len(actual_result)

        lower_list = 1
        upper_list = 5

        # This while loop will keep going until the user input in an valid digit to check
        # It will also handle the scrolling of the page
        while True:

            handle_scrolling(actual_result)
            print("Pick a item to check price")
            print("[Next] - Scroll for the next items")
            print("[Prev] - Go back to the previous items\n")

            # Then telling the user to input a choice from the menu
            user_input = input("Please enter in a command: ")

            # Increment the counter
            if user_input.lower() == "next":

                if upper_list + 5 > len(actual_result) and upper_list != len(actual_result):
                    lower_list = upper_list + 1
                    upper_list = len(actual_result)
                elif upper_list != len(actual_result):
                    lower_list = upper_list + 1
                    upper_list = upper_list + 5
            # Decrement the counter
            elif user_input.lower() == "prev":
                if upper_list == len(actual_result):
                    upper_list = lower_list - 1
                    lower_list = upper_list - 4
                if lower_list != 1:
                    upper_list = lower_list - 1
                    lower_list = lower_list - 5
            elif user_input.isdigit():

                int_input = int(user_input)

                if int_input >= lower_list and int_input <= upper_list:

                    # Setting all the necessary variables and passing down the app link to display_price
                    game_title = actual_result[int_input - 1].find_all("td")[2].text
                    app_type = actual_result[int_input - 1].find_all("td")[1].text
                    app_link = actual_result[int_input - 1].td.a['href']

                    break # Breaking the inner for loop

                else:
                    print("You did not enter in a valid item number")

            elif user_input == "":  # User wants to quit
                app_link = None

                break
            else:
                print("You did not enter a digit try again ", end="")

    except Exception as e:  # No results found

        print("\nNo results found\n")

    return app_link


def option_a():
    while True:

        input_game_title = input("Search for game: ")

        if input_game_title == '':  # User wants to be out
            break

        link = search_games(input_game_title)

        if link is None:
            break
        display_price(link)


def favorite_list():

    # Function that performs adding to the favorite list
    # This can let you add games to a watch list which gives you updates on the current price
    # and when you run the script the first time it will run through the games on your favorite list
    # to see whether there are discounts or not
    list_of_games = []

    # Read the list of games that is in the file first
    file = open("data.csv", "r")

    print(file.readline())

    # Need to go online and find title
    # Writing the file
    game_name = input("Which game would you like to add?: ")
    input_game_title = game_name.replace(" ", "+")  # Replace any spaces with percentage signs

    # Opening and getting the webpage source
    respond = Request(inquiry + input_game_title, headers={'User-Agent': 'XYZ/3.0'})
    response = urlopen(respond, timeout=5).read()

    soup = BeautifulSoup(response, 'lxml')

    search_games(game_name)

    file = open('data.csv', 'a')
    file.write(input("Game?: ")+"\n")

    for game in list_of_games:
        print(game)


def free_to_play():
    print("Not implemented yet")


# def start_up():


# Main loop
if __name__ == '__main__':

    while True:

        # Main menu options
        print("(A) - Search price for games")
        print("(B) - Favorite lists")
        print("(C) - Free to play games")
        menu_input = input("Enter in options: ")

        if menu_input.lower() == "a": # Search for pricing of games
            option_a()
        elif menu_input.lower() == "b":
            # favorite_list()
            print("kill me")
        elif menu_input.lower() == "c":
            # free_to_play()
            print("e")
        elif menu_input == "":
            break

