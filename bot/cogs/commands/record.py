import discord
from discord import app_commands
from discord.ext import commands

import logging

from bot.duel_helpers.duel_manager import DuelManager
from bot.util.accept_view import AcceptView

class Record(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
    
    @app_commands.command(name = "record", description = "Shows your fighting records!")
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def record(self, interaction : discord.Interaction):
        record = await self.bot.user_data.get_user(interaction.user.id)
        user = interaction.user

        descr_str = f'''
            ⭐Total Wins - {record["winstotal"]}
            🌟Unique Wins - {record["uniquewins"]}
            🎮Total Games - {record["gamestotal"]}
            🏳️Forfeits - {record["forfeitcount"]}
        '''
        embed = discord.Embed(description=descr_str)
        embed.set_author(name = f"{user.nick if user.nick else user.name} - Record", icon_url = user.avatar)
        embed.set_thumbnail(url = user.avatar)
        await interaction.response.send_message(embed = embed)
        print(await self.bot.user_record.get_user(user.id))
async def setup(bot) -> None:
    await bot.add_cog(Record(bot))