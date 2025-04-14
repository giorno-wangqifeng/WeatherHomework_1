import tkinter as tk
from tkinter import messagebox
from weather import Weather

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")

        self.api_key = "3fee99a5c32b8d8c66576b576670a821"  # 替换为你的 OpenWeatherMap API Key

        self.city_label = tk.Label(root, text="Enter city name:")
        self.city_label.pack()

        self.city_entry = tk.Entry(root)
        self.city_entry.pack()

        self.get_weather_button = tk.Button(root, text="Get Weather", command=self.get_weather)
        self.get_weather_button.pack()

        self.result_text = tk.Text(root, height=20, width=60)
        self.result_text.pack()

    def get_weather(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showwarning("Warning", "City name cannot be empty!")
            return

        weather = Weather(self.api_key, city)
        self.result_text.delete(1.0, tk.END)

        current_weather = weather.format_weather()
        self.result_text.insert(tk.END, current_weather + "\n\n")

        forecast = weather.format_forecast()
        self.result_text.insert(tk.END, forecast + "\n\n")

        alerts = weather.format_alerts()
        self.result_text.insert(tk.END, alerts + "\n\n")

        aqi = weather.format_aqi()
        self.result_text.insert(tk.END, aqi)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()