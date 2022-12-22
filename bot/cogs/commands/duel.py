import asyncio
import discord
from discord import app_commands
from discord.ext import commands

class Duel(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    def check_bot(interaction: discord.Interaction) -> bool:
        return interaction.user

    @app_commands.command(name = "duel", description = "Challenge another player to a duel!")
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def duel(self, interaction: discord.Interaction, user: discord.Member):
        if user.bot:
            await interaction.response.send_message("You can't challenge a bot! You'll definetly lose!", ephemeral=True)
            return
            
        
        player1, player2 = interaction.user, user
        await interaction.response.send_message("Insert duel here")
        return

    @duel.error
    async def on_duel_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await interaction.response.send_message(str(error))

async def setup(bot):
    await bot.add_cog(Duel(bot))