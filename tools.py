import requests
from config import URL

def update_data():

    response = requests.get(URL)
    with open("language_cards.db", "wb") as f:
        f.write(response.content)