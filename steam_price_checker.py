# ------
# import statements
# ------
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from art import tprint
import getpass

# Constants
max_display = 5
game_title = ""
app_type = ""
app_link = ""
app_before = 'https://steamdb.info'
app_sale_page = 'https://steamdb.info/sales/'
steam_store = 'https://store.steampowered.com/'

# Link with inquiry
inquiry = 'https://steamdb.info/search/?a=app&q='


def display_price(app_id_link):

    respond = Request(app_id_link, headers={'User-Agent': 'XYZ/3.0'})

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

        # Setting the upper_list to prevent user inputting higher number into search result
        # For 5 or less items
        if total_item <= max_display:
            upper_list = total_item

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

                if total_item > max_display:

                    if upper_list + 5 > len(actual_result) and upper_list != len(actual_result):
                        lower_list = upper_list + 1
                        upper_list = len(actual_result)
                    elif upper_list != len(actual_result):
                        lower_list = upper_list + 1
                        upper_list = upper_list + 5
            # Decrement the counter
            elif user_input.lower() == "prev":

                if total_item > max_display:
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
                    print("You did not enter in a valid item number", end="\n\n")

            elif user_input == "":  # User wants to quit
                app_link = None

                break
            else:
                print("You did not enter a digit try again ", end="\n\n")

    except Exception as e:  # No results found

        print("\nNo results found\n")

        app_link = None

    return app_link


def option_a():

    tprint("Search Game Price!", font="small")
    while True:

        input_game_title = input("Search for game: ")

        if input_game_title == '':  # User wants to be out
            break

        link = search_games(input_game_title)

        if link is None:
            break
        display_price(app_before+link)


def add_game_favorite():

    # Function that performs adding to the favorite list
    # This can let you add games to a watch list which gives you updates on the current price
    # and when you run the script the first time it will run through the games on your favorite list
    # to see whether there are discounts or not
    list_of_games = []

    # Read the list of games that is in the file first
    file = open("data.txt", "r", errors="ignore")

    while True:

        # Need to go online and find title
        # Writing the file
        game_name = input("Which game would you like to add?: ")
        input_game_title = game_name.replace(" ", "+")  # Replace any spaces with percentage signs

        if input_game_title == "":

            # User wants to quit
            break
        else:

            # Opening and getting the webpage source
            respond = Request(inquiry + input_game_title, headers={'User-Agent': 'XYZ/3.0'})
            response = urlopen(respond, timeout=5).read()

            soup = BeautifulSoup(response, 'html.parser')

            link = search_games(game_name)

            # Make sure that the link returned from search is not None before we write it into the file
            if link is not None:

                text = "[" + game_title + "]:"+ app_before + link

                file = open("data.txt", "a", encoding='utf-8')
                file.write(text + "\n")

                print(game_title, "have been successfully added to your favorite list", end="\n\n")

    file.close()

def print_favorite_list_with_price():

    file = open("data.txt", "r+", encoding="utf-8-sig", errors="ignore")
    file_array = file.read().splitlines()

    tprint("Favorite   List!", font="small")
    print("Fetching data...", end="\n\n")
    output = ""

    if len(file_array) == 0:
        print("There are no games in your favorite list :(", end="\n\n")
    else:

        global counter
        counter = 1

        for line in file_array:

            if file_array[len(file_array)-1] == line:

                # Last item
                line = line.strip("\n")
                r_bracket = line.rfind("]")
                link = line[r_bracket + 2:]
                output += str(counter) + ". " + line[0:r_bracket + 1] + " is currently " + get_link_price(link) + "\n"
                counter += 1
            else:

                # Not last item
                line = line.strip("\n")
                r_bracket = line.rfind("]")
                link = line[r_bracket+2:]
                output += str(counter) + ". " + line[0:r_bracket + 1] + " is currently " + get_link_price(link) + "\n\n"
                counter += 1

        print(output)
    file.close()


def print_favorite_list():

    file = open("data.txt", "r+", encoding="utf-8-sig", errors="ignore")
    file_array = file.read().splitlines()

    if len(file_array) == 0:
        pass
    else:

        global counter
        counter = 1
        tprint("Favorite List!", font="small")
        output = ""

        for line in file_array:

            if file_array[len(file_array) - 1] == line:

                line = line.strip("\n")
                r_bracket = line.rfind("]")
                output += str(counter) + ". " + line[0:r_bracket+1] + "\n"
                counter += 1
            else:

                line = line.strip("\n")
                r_bracket = line.rfind("]")
                output += str(counter) + ". " + line[0:r_bracket+1] + "\n\n"
                counter += 1

        print(output)

    file.close()

    return len(file_array)


def get_link_lowest_price(link):
    # Given a SteamApp link return a String representing the lowest price of the given game
    # Opening and getting the webpage source
    respond = Request(link, headers={'User-Agent': 'XYZ/3.0'})
    response = urlopen(respond, timeout=5).read()

    # Putting it through beautifulsoup and getting the soup object
    soup = BeautifulSoup(response, 'lxml')

    price_table = soup.find('table', class_="table table-fixed table-prices table-hover table-sortable")
    current_row = price_table.find('tr', class_="table-prices-current")
    tds = current_row.find_all('td')

    return tds[3].text


def get_link_price(link):

    # Given a SteamApp link return a String representing the price of the given game
    # Opening and getting the webpage source
    respond = Request(link, headers={'User-Agent': 'XYZ/3.0'})
    response = urlopen(respond, timeout=5).read()

    # Putting it through beautifulsoup and getting the soup object
    soup = BeautifulSoup(response, 'lxml')

    price_table = soup.find('table', class_="table table-fixed table-prices table-hover table-sortable")
    current_row = price_table.find('tr', class_="table-prices-current")
    tds = current_row.find_all('td')

    return tds[1].text


def remove_game(index_to_delete):

    # This function will be removing game from the favorite list
    # Getting the lines and putting it into an array
    file = open('data.txt', 'r', encoding="utf-8-sig", errors="ignore")
    lines = file.readlines()
    file.close()

    removed_game_title = lines[index_to_delete]

    del lines[index_to_delete]

    file = open('data.txt', 'w')
    for line in lines:
        file.write(line)

    file.close()

    return removed_game_title


def ask_game_to_remove():

    global counter

    results = print_favorite_list()

    if results == 0:
        print("There are no games in your favorite list :(", end="\n\n")
    else:

        # Make sure the input_index is valid
        while True:

            input_index = input("Which game would you like to remove from your favorite list?: ")

            if input_index == "":
                break
            elif not input_index.isdigit():
                print()
                print("You must enter in an digit to remove a game", end="\n\n")
            elif int(input_index) < counter and int(input_index) >= 1:

                removed_game = remove_game(int(input_index) - 1)

                removed_game = removed_game[0:removed_game.find("]") + 1]

                print()
                print(removed_game, "have been successfully removed from your favorite game", end="\n\n")

                break
            else:
                print()
                print("Invalid game to remove from the favorite list", end="\n\n")


def introduction():

    tprint("Steam Price Checker", font="small")
    tprint("Welcome...", font="small")
    tprint(getpass.getuser(), font="small")

def favorite_list_intro():

    tprint("Favorite List Menu", font="small")


def option_b():

    favorite_list_intro()

    while True:

        print("(A) - Check price of your favorite list")
        print("(B) - Add new game to favorite list")
        print("(C) - Remove a game from favorite list")
        print("(D) - What is on my favorite list?")
        user_choice = input("What would you like to do?: ")
        print()

        if user_choice.lower() == 'a':
            print_favorite_list_with_price()
        elif user_choice.lower() == 'b':
            add_game_favorite()
        elif user_choice.lower() == 'c':
            ask_game_to_remove()
        elif user_choice.lower() == 'd':
            print_favorite_list()
        elif user_choice.lower() == '': # User want to quit
            break


def free_to_play():

    # Returns the list of play for free games with their link in a dictionary
    respond = Request(app_sale_page, headers={'User-Agent': 'XYZ/3.0'})

    response = urlopen(respond, timeout=3).read()

    # Parsing into soup
    soup = BeautifulSoup(response, 'lxml')

    table = soup.find('table')

    trs = table.find_all('tr')

    # Creating a dictionary that will hold all of the free games and the link it is associated with
    output = dict()

    for tr in trs:

        # Play for free row traits
        if tr.find('span', class_="category sales-play-for-free") is not None:

            tds = tr.find_all('td')
            game_name = tds[2].a.text
            game_link = steam_store + tds[2].a["href"]

            output[game_name] = game_link

    return output


def free_game_intro():

    # Intro for the free game
    tprint("Play For Free Games!", font="small")


def option_c():

    free_game_intro()

    print("Fetching data...", end="\n\n")

    # Gather the list of free to play games
    play_free_games = free_to_play()

    if play_free_games.__len__() == 0:
        print("There are no play for free games right now :(", end="\n\n")
    else:

        game_counter = 1
        str_output = ""

        for key in play_free_games:
            str_output += str(game_counter) + ". " + "[" + key + "]: " + play_free_games[key] + "\n"
            game_counter += 1

        print(str_output)


def start_up():

    # When the program is ranned we will call the start_up method, which contains introduction
    # And running the favorite list check
    introduction()

    file = open("data.txt", "r", encoding="utf-8-sig", errors="ignore")
    file_array = file.readlines()

    if len(file_array) != 0:

        # We only print if the file is not empty
        print_favorite_list_with_price()

# Main loop
def main():

    introduction()

    while True:

        # Main menu options
        print("(A) - Search price for games")
        print("(B) - Favorite lists")
        print("(C) - Free to play games")
        print("Enter in option: ", end="")
        menu_input = input()
        print()

        if menu_input.lower() == "a": # Search for pricing of games
            option_a()
        elif menu_input.lower() == "b":
            option_b()
        elif menu_input.lower() == "c":
            option_c()
        elif menu_input == "":
            break

if __name__ == "__main__":

    main()