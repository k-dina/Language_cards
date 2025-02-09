import requests
from config import URL
from pathlib import Path
import appdirs


app_name = "English Learning Game"
app_data_path = Path(appdirs.user_data_dir(appname=app_name, appauthor="Ksusha"))

if not app_data_path.exists():
    app_data_path.mkdir(parents=True, exist_ok=True)

FILE_PATH = app_data_path / "language_cards.db"




def update_data():
    response = requests.get(URL)
    with open(FILE_PATH, "wb") as f:
        f.write(response.content)

