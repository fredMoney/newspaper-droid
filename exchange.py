import feedparser


class ExchangeRates():
    def __init__(self):
        self.currencies = ["200003_EUR", "200004_USD"]
        self.URL = "https://bnro.ro/RSS_200003_EUR.aspx"

            
    def getRates(self):
        rates = []
        for currency in self.currencies:
            feed = feedparser.parse(f"https://bnro.ro/RSS_{currency}.aspx")
            rates.append(feed.entries[0].title[:18].strip())
        return rates

