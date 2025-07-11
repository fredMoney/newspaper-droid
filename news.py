import requests
from bs4 import BeautifulSoup
import re

URL = "https://www.digi24.ro/"
response = requests.get(URL)

class NewsCrawler:
    class Article:
        def __init__(self, title, intro, link, thumb):
            self.title = "" if title is None else title.text.strip()
            self.intro = "" if intro is None else intro.text.strip()
            self.link  = "" if link is None else link.strip()
            self.thumb = "" if thumb is None else thumb["src"].strip()


    def __init__(self):
        self.soup = BeautifulSoup(response.content, "html.parser")
        self.news  = []

    def readNews(self) -> None:
        articles = self.soup.find_all("article", class_="article")
        news = []
        for article in articles:
            title = article.find(re.compile("h[234]"), class_="article-title").a
            intro = article.find("p", class_="article-intro")
            link  = URL + title["href"][1:]
            thumb = article.find("img")

            news.append(NewsCrawler.Article(title, intro, link, thumb))
        self.news = news

    def getTitles(self, count=3) -> list:
        return [article.title for article in self.news[:count]]

    def getArticles(self, count=3) -> list:
        return self.news[:count]

    def getArticle(self, article) -> Article:
        return self.news[article]

c = NewsCrawler()
c.readNews()
