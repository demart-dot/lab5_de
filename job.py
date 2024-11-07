import requests
import json
from pathlib import Path

class MetalPriceJob:
    def __init__(self, raw_dir):
        self.raw_dir = Path(raw_dir)  # Використовуємо pathlib для роботи з шляхами

    def clear_directory(self, path):
        if path.exists():
            for file in path.iterdir():
                if file.is_file():
                    file.unlink()

    def fetch_data(self):
        url = "https://metal-price-tracker-default-rtdb.firebaseio.com/metals.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return []

    def save_data(self, data, date, feature):
        feature_path = self.raw_dir / feature / date
        feature_path.mkdir(parents=True, exist_ok=True)  # Створюємо всі батьківські каталоги, якщо їх немає
        self.clear_directory(feature_path)

        filepath = feature_path / f"{date}.json"
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

        return [filepath]

    def run(self, date, feature):
        data = self.fetch_data()
        if not data:
            print("No data fetched, exiting.")
            return []

        # Фільтрація даних за датою
        filtered_data = [entry for entry in data if entry["Date"] == date]
        
        if not filtered_data:
            print(f"No data found for date: {date}")
            return []

        # Збереження даних в файл
        return self.save_data(filtered_data, date, feature)

# Приклад використання
raw_dir = "path_to_raw_data"
job = MetalPriceJob(raw_dir)
job.run("2024-10-25", "gold")