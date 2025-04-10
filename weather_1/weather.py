import requests
import json
import matplotlib.pyplot as plt

class Weather:
    def __init__(self, api_key, city):
        self.api_key = api_key
        self.city = city
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
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

    def get_forecast_data(self):
        """获取未来几天的天气预报"""
        params = {
            "q": self.city,
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(self.forecast_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Unable to fetch forecast data. Status code: {response.status_code}")
            return None

    def get_aqi_data(self, lat, lon):
        """获取空气质量指数（AQI）"""
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

            # 获取经纬度并显示 AQI
            lat = data["coord"]["lat"]
            lon = data["coord"]["lon"]
            self.display_aqi(lat, lon)

    def display_forecast(self):
        """展示未来几天的天气预报"""
        forecast_data = self.get_forecast_data()
        if forecast_data:
            print("\nWeather Forecast for the next few days:")
            forecast_list = forecast_data["list"]
            forecast_days = {}
            for forecast in forecast_list:
                date = forecast["dt_txt"].split(" ")[0]  # 提取日期部分
                if date not in forecast_days:
                    forecast_days[date] = []
                forecast_days[date].append({
                    "time": forecast["dt_txt"].split(" ")[1],
                    "description": forecast["weather"][0]["description"],
                    "temperature": forecast["main"]["temp"]
                })

            # 打印每天的天气预报
            for date, forecasts in forecast_days.items():
                print(f"\n{date}:")
                for forecast in forecasts:
                    print(f"  {forecast['time']}: {forecast['description']}, Temperature: {forecast['temperature']}°C")

    def display_alerts(self):
        """展示天气预警信息"""
        forecast_data = self.get_forecast_data()
        if forecast_data:
            alerts = []
            for forecast in forecast_data["list"]:
                weather_description = forecast["weather"][0]["description"]
                if "rain" in weather_description or "thunderstorm" in weather_description:
                    alerts.append({
                        "time": forecast["dt_txt"],
                        "description": weather_description
                    })

            if alerts:
                print("\nWeather Alerts:")
                for alert in alerts:
                    print(f"{alert['time']}: {alert['description']}")
            else:
                print("\nNo weather alerts at the moment.")

    def display_aqi(self, lat, lon):
        """展示空气质量指数（AQI）"""
        aqi_data = self.get_aqi_data(lat, lon)
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