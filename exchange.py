import feedparser
import requests
from bs4 import BeautifulSoup

DEFAULT_CURRENCIES = ["EUR", "USD"]

class ExchangeRates():
    def __init__(self):
        self.currencies = {}
        self.URL = "https://bnro.ro/Cursul-de-schimb-524.aspx"
        response = requests.get(self.URL)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_="cursTable").tbody
        rows = table.find_all("tr")
        for row in rows:
            currency = row.find("td", class_="c2").text
            link = row.find_next("a")["href"]
            self.currencies[currency] = link
        self.followedCurrencies = DEFAULT_CURRENCIES


    def addFollowedCurrencies(self, currencies: list) -> None:
        for currency in currencies:
            if currency in self.currencies and currency not in self.followedCurrencies:
                self.followedCurrencies.append(currency)

    def removeFollowedCurrencies(self, currencies: list) -> None:
        for currency in currencies:
            if currency in self.followedCurrencies:
                self.followedCurrencies.remove(currency)

            
    def getRates(self):
        rates = []
        for currency in self.followedCurrencies:
            feed = feedparser.parse(f"https://bnro.ro/{self.currencies[currency]}")
            rates.append(feed.entries[0].title[:18].strip())
        return rates

e = ExchangeRates()
e.getRates()
