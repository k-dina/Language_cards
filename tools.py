import requests
from config import URL

def fetch_data():

    response = requests.get(URL)
    with open("language_cards.db", "wb") as f:
        f.write(response.content)

