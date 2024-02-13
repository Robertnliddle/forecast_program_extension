import datetime
import requests


class Forecast:

    def __init__(self):
        self.results = {}

    def __setitem__(self, date, value):
        self.results[date] = value

    def __getitem__(self, date):
        return self.results.get(date)

    def __iter__(self):
        return iter(self.results)

    def items(self):
        for date, value in self.results.items():
            return date,value


api_documentation = "https://open-meteo.com/en/docs"

query_results = "query_results.txt"


def save_query_file(date, result):
    with open(query_results, "a") as f:
        f.write(f"{date} / {result}\n")


def read_query_file():
    weather = {}
    with open(query_results, "r") as f:
        for line in f:
            date,value = line.strip().split(" / ")
            weather[date] = float(value)
    return weather


def get_weather(latitude, longitude, provided_date):
    api_endpoint = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=" \
                   f"precipitation_sum&timezone=Europe%2FLondon&start_date={provided_date}&end_date={provided_date}"

    response = requests.get(api_endpoint).json()
    return response["daily"]["precipitation_sum"][0]


def rain_or_not(weather_report):
    if weather_report > 0.0:
        print(f"It will rain {weather_report} mm")
    elif weather_report == 0.0:
        print("It will not rain")
    else:
        print("I don't know")


# ask the user for the date
today = datetime.date.today()
provided_date = input("Enter a date in YYYY-mm-dd format or press enter to see the next day: ")

if not provided_date:
    next_day = datetime.date.today() + datetime.timedelta(days=1)
    provided_date = next_day.strftime("%Y-%m-%d")

latitude = 35.917973
longitude = 14.409943

weather = read_query_file()
if provided_date in weather:
    rain_or_not(weather[provided_date])
else:
    expected_weather = get_weather(latitude, longitude, provided_date)
    save_query_file(provided_date, expected_weather)
    rain_or_not(expected_weather)

