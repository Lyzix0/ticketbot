import nextcord
from discord.ext import commands

from cogs.base import BaseCog
from cogs.tickets import TicketStartHandler


class ChannelMessage(BaseCog):
    def __init__(self, bot, ticket_handler: TicketStartHandler):
        super().__init__(bot)
        self.ticket_handler = ticket_handler

    # команда *start_ticketing #chat для создания сообщения
    @commands.command()
    async def start_ticketing(self, ctx, chat: nextcord.TextChannel):
        if chat is None:
            await ctx.send(f"Канал не найден.")
            return

        view = self.ticket_handler.create_ticket_button()

        await chat.send(
            "Возникают проблемы с работой сервера или есть вопросы? Напишите об этом нам!",
            view=view,
        )
        await ctx.reply("Тикетинг был начат!")

    # обработчик ошибок
    @start_ticketing.error
    async def start_ticketing_error(self, ctx, error: commands.CommandError):
        if isinstance(error, commands.CommandError):
            return await ctx.send("Введите правильный ID канала!")


def setup(bot):
    ticket_handler = TicketStartHandler(bot)
    bot.add_cog(ChannelMessage(bot, ticket_handler))
