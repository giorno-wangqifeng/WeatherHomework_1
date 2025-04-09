import requests
import json
import matplotlib.pyplot as plt

class Weather:
    def __init__(self, api_key, city):
        self.api_key = api_key
        self.city = city
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather_data(self):
        params = {
            "q": self.city,
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Unable to fetch weather data. Status code: {response.status_code}")
            return None

    def display_weather(self):
        data = self.get_weather_data()
        if data:
            city = data["name"]
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            print(f"Weather in {city}:")
            print(f"Description: {weather_description}")
            print(f"Temperature: {temperature}°C")
            print(f"Humidity: {humidity}%")
            print(f"Wind Speed: {wind_speed} m/s")

            self.plot_weather_data(temperature, humidity)

    def plot_weather_data(self, temperature, humidity):
        labels = ["Temperature (°C)", "Humidity (%)"]
        values = [temperature, humidity]

        plt.bar(labels, values, color=["blue", "green"])
        plt.xlabel("Weather Metrics")
        plt.ylabel("Values")
        plt.title(f"Weather in {self.city}")
        plt.show()