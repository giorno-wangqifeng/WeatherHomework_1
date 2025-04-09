from weather import Weather

def main():
    api_key = "3fee99a5c32b8d8c66576b576670a821"  # 替换为你的 OpenWeatherMap API Key
    city = input("Enter the city name: ")

    weather = Weather(api_key, city)
    weather.display_weather()

if __name__ == "__main__":
    main()