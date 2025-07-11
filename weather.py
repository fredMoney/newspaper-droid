import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import collections

class WeatherHandler():
    def __init__(self):
        load_dotenv()
        self.TOKEN = os.getenv("WEATHER_API_KEY")
        self.location = "Bucharest"
        self.date = datetime.today().strftime("%Y-%m-%d")
        self.scale = "C"

    def getWeather(self):
        response = requests.get(
                    f"https://api.worldweatheronline.com/premium/v1/weather.ashx?key={self.TOKEN}&q={self.location}"
                   )
        parser = BeautifulSoup(response.content, "xml")
        today = parser.find("date", string=f"{self.date}").parent

        tempAverage = today.find(f"avgtemp{self.scale}")
        tempHigh    = today.find(f"maxtemp{self.scale}")
        tempLow     = today.find(f"mintemp{self.scale}")
        weather     = parser.find("current_condition").weatherDesc
        hourly      = today.find_all("hourly")
        weatherDesc = [ hour.find("weatherDesc").text for hour in hourly[2:] ]
        weatherCounter = collections.Counter(weatherDesc)

        return f"{weather.text}, average: {tempAverage.text}° {self.scale}, {weatherCounter.most_common(1)[0][0]}, min: {tempLow.text}° {self.scale}, max: {tempHigh.text}° {self.scale}"
