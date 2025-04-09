import requests
import json
import matplotlib.pyplot as plt

class Weather:
    def __init__(self, api_key, city):
        self.api_key = api_key
        self.city = city
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.aqi_url = "http://api.openweathermap.org/data/2.5/air_pollution"

    def get_weather_data(self):
        """获取当前天气数据"""
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

    def get_aqi_data(self):
        """获取空气质量指数（AQI）"""
        # 获取当前天气数据以获取经纬度
        weather_data = self.get_weather_data()
        if not weather_data:
            return None

        lat = weather_data["coord"]["lat"]
        lon = weather_data["coord"]["lon"]

        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key
        }
        response = requests.get(self.aqi_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Unable to fetch AQI data. Status code: {response.status_code}")
            return None

    def display_weather(self):
        """展示当前天气信息"""
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

    def display_aqi(self):
        """展示空气质量指数（AQI）"""
        aqi_data = self.get_aqi_data()
        if aqi_data:
            aqi = aqi_data["list"][0]["main"]["aqi"]
            components = aqi_data["list"][0]["components"]
            print("\nAir Quality Index (AQI):")
            print(f"AQI: {aqi}")
            print("Components:")
            for key, value in components.items():
                print(f"{key}: {value}")

    def plot_weather_data(self, temperature, humidity):
        """绘制温度和湿度的柱状图"""
        labels = ["Temperature (°C)", "Humidity (%)"]
        values = [temperature, humidity]

        plt.bar(labels, values, color=["blue", "green"])
        plt.xlabel("Weather Metrics")
        plt.ylabel("Values")
        plt.title(f"Weather in {self.city}")
        plt.show()