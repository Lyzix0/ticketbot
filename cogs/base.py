from nextcord.ext import commands


class BaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Ког {self.__class__.__name__} готов")


def setup(bot):
    bot.add_cog(BaseCog(bot))
