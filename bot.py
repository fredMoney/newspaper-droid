import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging
from news import NewsCrawler
from exchange import ExchangeRates
from weather import WeatherHandler


handler = logging.FileHandler(filename="bot.log", encoding="utf-8", mode="w")

class DigestBot(commands.Bot):
    def __init__(self):
        load_dotenv()
        self.TOKEN = os.getenv("DISCORD_API_KEY")
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="+", intents=intents)
        self.MAX_ARTICLES = 20
        self.newsCrawler = NewsCrawler()
        self.exchangeHandler = ExchangeRates()
        self.weatherHandler = WeatherHandler()

    def update(self) -> None:
        self.newsCrawler.readNews()


bot = DigestBot()
bot.update()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(f"Message from {message.author}: {message.content}")
    await bot.process_commands(message)


# DIGEST
@bot.command(name="digest")
async def digest(ctx):
    titles  = "\n".join(bot.newsCrawler.getTitles())
    rates   = "\n".join(bot.exchangeHandler.getRates())
    weather = bot.weatherHandler.getWeather()
    await ctx.send(f"{titles}\n{rates}\n{weather}")


# NEWS
@bot.command(name="news")
async def news(ctx):
    embed = discord.Embed(title="NEWS")
    for article in bot.newsCrawler.getArticles(count=5):
        embed.add_field(name=f"{article.title}", value=f"{article.intro}")
    await ctx.send(embed=embed)

@bot.command(name="n")
async def newsArticle(ctx, arg):
    article = bot.newsCrawler.getArticle(article=int(arg)-1)
    embed = discord.Embed(title=f"{article.title}", url=f"{article.link}", description=f"{article.intro}")
    embed.set_thumbnail(url=f"{article.thumb}")
    await ctx.send(embed=embed)


# EXCHANGE
@bot.command(name="rates")
async def rates(ctx):
    return


bot.run(f"{bot.TOKEN}", log_handler=handler, log_level=logging.DEBUG)
