import os

import nextcord
from nextcord.ext import commands

from config import BOT_TOKEN

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="*", intents=intents)


@bot.event
async def on_ready():
    print(f"Бот запущен {bot.user}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
