import requests
from bs4 import BeautifulSoup
import sys

number_of_listings = 5

# Args
if (len(sys.argv) < 4):
    print("Usage : python strava.py jmeno heslo jidelna")
    sys.exit(1)

# Start the session
session = requests.Session()

# Create the payload
payload = {'uzivatel' : sys.argv[1],
          'heslo' : sys.argv[2],
          'zarizeni' : sys.argv[3]
        }

# Post the payload to the site to log in
s = session.post("https://www.strava.cz/Strava/Stravnik/prihlaseni", data=payload)

# Navigate to the next page and scrape the data
s = session.get('https://www.strava.cz/Strava/Stravnik/Objednavky')

#Parse
soup = BeautifulSoup(s.text, 'html.parser')
res = soup.find_all(class_="objednavka-obalka objednavka-obalka-jednotne")

# For the first `number_of_listings` listings
for x in res[:number_of_listings]:

    # Get the day and print
    day = x.find("div").find("div").text.split('\n')[1].split('\r')[0].lstrip()
    print(day)

    # Find all the foods 
    foods = x.find_all(class_="objednavka-jidla-obalka")[0].find_all(class_="objednavka-jidlo-obalka")
    for food in foods:
        # Find the values
        food_name = food.find(class_="objednavka-jidlo-nazev").text
        food_type = food.find(class_="objednavka-jidlo-popis").text
        food_value = food.find(class_="objednavka-jidlo-zmena").contents[1].contents[3].attrs["value"]

        # Remove this if you need to
        # This just removes the soup entry
        if(food_type == "Polévka"):
            continue

        # Turn the value from text to markdown-like text
        if food_value == "zaskrtnuto":
            food_value = "[x]"
        elif food_value == "nezaskrtnuto":
            food_value = "[ ]"
        else:
            food_value = "[-]"
        
        # Strip in case of leading/trailing spaces and print
        print((food_value + " " + food_type + " - " + food_name).lstrip().rstrip())

    # Empty line for cleanness
    print()