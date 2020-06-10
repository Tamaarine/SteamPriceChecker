# ------
# import statements
# ------
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import csv
"""
Game, DLC type will have prices. Keep in mind there is also future games and free games that won't have price
Legacy media, Unknown, Demo, Tool will not have prices
"""

# Constants
max_display = 5
game_title = ""
app_type = ""

# Link with inquiry
inquiry = 'https://steamdb.info/search/?a=app&q='

# Testing out csv first
csv_file = open('../../Downloads/data.csv', 'w')

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


# Main loop
if __name__ == '__main__':

    while True:

        # Asking for input
        game_title = input("Search for game: ")

        if game_title == '': # User wants to be out
            break

        game_title = game_title.replace(" ", "+") # Replace any spaces with percentage signs

        # Opening and getting the webpage source
        respond = Request(inquiry+game_title, headers={'User-Agent': 'XYZ/3.0'})

        response = urlopen(respond, timeout=3).read()

        # Putting it through beautifulsoup and getting the soup object
        soup = BeautifulSoup(response, 'lxml')

        # Finding the result table
        table = soup.find('table', class_="table-bordered")

        try:    # Next find the results in a try block

            actual_result = table.find_all('tr', class_="app")

            print()  # To clear up the space before

            if len(actual_result) <= max_display:

                for i in range(len(actual_result)):
                    print("[", i + 1, "]", actual_result[i].find_all("td")[2].text, "\n")

            else:

                for i in range(0, max_display):
                    print("[", i + 1, "]", actual_result[i].find_all("td")[2].text, "\n")

        except Exception as e:    # No results found

            print("\nNo results found\n")

        print("Which game would you like to check?: ", end="")
        while True:

            # Then telling the user to input a choice from the menu
            to_check = input()

            if to_check.isdigit():
                break
            elif to_check == "": # User wants to quit
                break
            else:
                print("You did not enter a digit try again ", end="")

        # Setting all the necessary variables and passing down the app link to display_price
        game_title = actual_result[int(to_check)-1].find_all("td")[2].text
        app_type = actual_result[int(to_check)-1].find_all("td")[1].text
        app_link = actual_result[int(to_check)-1].td.a['href']
        display_price(app_link)
