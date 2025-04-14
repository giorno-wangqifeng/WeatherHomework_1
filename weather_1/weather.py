import requests
import json

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
            return {"error": f"Unable to fetch weather data. Status code: {response.status_code}"}

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
            return {"error": f"Unable to fetch forecast data. Status code: {response.status_code}"}

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
            return {"error": f"Unable to fetch AQI data. Status code: {response.status_code}"}

    def format_weather(self):
        """格式化当前天气信息"""
        data = self.get_weather_data()
        if "error" in data:
            return data["error"]

        city = data["name"]
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        return (f"Weather in {city}:\n"
                f"Description: {weather_description}\n"
                f"Temperature: {temperature}°C\n"
                f"Humidity: {humidity}%\n"
                f"Wind Speed: {wind_speed} m/s")

    def format_forecast(self):
        """格式化未来几天的天气预报"""
        forecast_data = self.get_forecast_data()
        if "error" in forecast_data:
            return forecast_data["error"]

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

        forecast_text = "Weather Forecast for the next few days:\n"
        for date, forecasts in forecast_days.items():
            forecast_text += f"\n{date}:\n"
            for forecast in forecasts:
                forecast_text += (f"  {forecast['time']}: {forecast['description']}, "
                                  f"Temperature: {forecast['temperature']}°C\n")
        return forecast_text

    def format_alerts(self):
        """格式化天气预警信息"""
        forecast_data = self.get_forecast_data()
        if "error" in forecast_data:
            return forecast_data["error"]

        alerts = []
        for forecast in forecast_data["list"]:
            weather_description = forecast["weather"][0]["description"]
            if "rain" in weather_description or "thunderstorm" in weather_description:
                alerts.append({
                    "time": forecast["dt_txt"],
                    "description": weather_description
                })

        if alerts:
            alert_text = "Weather Alerts:\n"
            for alert in alerts:
                alert_text += f"{alert['time']}: {alert['description']}\n"
            return alert_text
        else:
            return "No weather alerts at the moment."

    def format_aqi(self):
        """格式化空气质量指数（AQI）"""
        data = self.get_weather_data()
        if "error" in data:
            return data["error"]

        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]
        aqi_data = self.get_aqi_data(lat, lon)
        if "error" in aqi_data:
            return aqi_data["error"]

        aqi = aqi_data["list"][0]["main"]["aqi"]
        components = aqi_data["list"][0]["components"]

        aqi_text = "Air Quality Index (AQI):\n"
        aqi_text += f"AQI: {aqi}\n"
        aqi_text += "Components:\n"
        for key, value in components.items():
            aqi_text += f"{key}: {value}\n"
        return aqi_text