import requests
from config import URL
from pathlib import Path
import appdirs

# Получаем путь к папке Application Support
app_name = "English Learning Game"  # Замените на имя вашего приложения
app_data_path = Path(appdirs.user_data_dir(appname=app_name, appauthor="Ksusha"))

# Создаем папку, если ее нет
if not app_data_path.exists():
    app_data_path.mkdir(parents=True, exist_ok=True)

# Пример записи файла в эту папку
FILE_PATH = app_data_path / "language_cards.db"




def update_data():
    response = requests.get(URL)
    with open(FILE_PATH, "wb") as f:
        f.write(response.content)

