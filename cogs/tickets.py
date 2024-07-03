import asyncio

import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View


class TicketStartHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def button_callback(self, interaction: nextcord.Interaction):
        guild = interaction.guild
        category = nextcord.utils.get(guild.categories, name="Тикеты")

        if category is None:
            category = await guild.create_category("Тикеты")
        else:
            channels = [i.name[7:] for i in category.channels]
            if interaction.user.name in channels:
                await interaction.response.send_message(
                    f"У вас есть незакрытый тикет. Вы не можете создать еще один, пока не закроете старый",
                    ephemeral=True,
                )
                return

        # необходимые права, чтобы видеть канал с тикетом (нужно доделать)
        overwrites = {
            guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            guild.me: nextcord.PermissionOverwrite(read_messages=True),
        }

        channel_name = f"ticket-{interaction.user.name}"
        ticket_channel = await guild.create_text_channel(
            channel_name, category=category, overwrites=overwrites
        )

        await ticket_channel.send(
            f"Здравствуйте! Пожалуйста, предоставьте все необходимые док-ва для рассмотрения жалобы,"
            f" {interaction.user.mention}!"
        )
        ticket = TicketHandler(bot=self.bot)
        await ticket_channel.send(
            "Проблема решена?", view=ticket.create_close_ticket_button(ticket_channel)
        )

        await interaction.response.send_message(
            f"Тикет канал создан: {ticket_channel.mention}. Опишите свою проблему в нем",
            ephemeral=True,
        )

    def create_ticket_button(self):
        button = Button(label="Создать тикет", style=nextcord.ButtonStyle.primary)
        button.callback = self.button_callback
        view = View()
        view.add_item(button)
        return view


class TicketHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # создает кнопку для закрытия в тикет-канале
    def create_close_ticket_button(self, ticket_channel):
        apply_button = Button(label="Закрыть тикет", style=nextcord.ButtonStyle.primary)
        apply_button.callback = lambda interaction: self.close_ticket_apply(
            interaction, ticket_channel
        )
        view = View()
        view.add_item(apply_button)
        return view

    # подтверждение на закрытие тикета
    async def close_ticket_apply(
        self, interaction: nextcord.Interaction, ticket_channel
    ):
        close_button = Button(label="Да, закрыть", style=nextcord.ButtonStyle.danger)
        close_button.callback = lambda inter: self.close_ticket(
            interaction, ticket_channel
        )
        view = View()
        view.add_item(close_button)

        await interaction.edit(
            content="Вы уверены что хотите закрыть тикет?", view=view
        )

    # закрывает тикет
    async def close_ticket(self, interaction, ticket_channel):
        await ticket_channel.send("Тикет закроется через 5 секунд!")
        await interaction.delete_original_message()
        await asyncio.sleep(5)
        await ticket_channel.delete()
        await interaction.followup.send("Тикет закрыт и удален.", ephemeral=True)


def setup(bot):
    bot.add_cog(TicketStartHandler(bot))
