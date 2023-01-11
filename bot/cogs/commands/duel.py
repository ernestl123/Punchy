import discord
from discord import app_commands
from discord.ext import commands

import traceback
import json
import asyncio

from bot.duel_helpers.duel_manager import DuelManager

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

        manager = DuelManager(player1, player2, interaction)
        
        await manager.run_game()
        return

    @duel.error
    async def on_duel_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await interaction.channel.send(str(error))
        traceback.print_exc()

    @app_commands.command(name = "test", description= "yeet")
    async def test(self, interaction : discord.Interaction):
        print("testing")
        with open("basic_duel_message.json", 'r') as f:
            gifs_dict = json.load(f)
        
        for move, message_dict in gifs_dict.items():
            print(move)
            for message, gif in message_dict.items():
                embed = discord.Embed(title = f"{move} - {message}").set_image(url = gif)
                await interaction.channel.send(embed = embed)
                await asyncio.sleep(5)
        
        
async def setup(bot):
    await bot.add_cog(Duel(bot))