
import os
import sqlite3
import requests


class OpenMeteoAPI:
    def __init__(self):
        self.latitude = 42.1015
        self.longitude = -72.5898

        self.api_url = "https://api.open-meteo.com/v1/forecast"

        self.db_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "db",
                "campusconnect.db"
            )
        )

    def get_weather(self):
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "wind_speed_10m"
            ],
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph"
        }

        try:
            response = requests.get(
                self.api_url,
                params=params,
                timeout=20
            )
            response.raise_for_status()

            return response.json()

        except requests.RequestException as error:
            print(f"Error accessing Open-Meteo API: {error}")
            return None

    def save_data(self, weather):
        if not weather or "current" not in weather:
            return

        current = weather["current"]

        description = (
            f"Temperature: {current.get('temperature_2m')} °F. "
            f"Feels like: {current.get('apparent_temperature')} °F. "
            f"Humidity: {current.get('relative_humidity_2m')}%. "
            f"Wind speed: {current.get('wind_speed_10m')} mph."
        )

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(
                "DELETE FROM api_data WHERE category = ?",
                ("Weather",)
            )

            cursor.execute("""
                INSERT INTO api_data
                (title, description, category, source_url)
                VALUES (?, ?, ?, ?)
            """, (
                "Current Weather - Springfield, MA",
                description,
                "Weather",
                self.api_url
            ))

            conn.commit()
            print("Weather data saved successfully!")

        finally:
            conn.close()

    def run(self):
        weather = self.get_weather()

        if weather:
            self.save_data(weather)

        return weather
