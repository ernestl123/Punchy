import discord
from discord import app_commands
from discord.ext import commands

import logging

from bot.duel_helpers.duel_manager import DuelManager
from bot.util.accept_view import AcceptView

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

        accept_view = AcceptView(user)
        embed = discord.Embed(description=f"{user.mention}, {interaction.user.mention} has challenged you to an honorable duel. Do you accept?")

        await interaction.response.send_message(embed = embed, view=accept_view)

        await accept_view.wait()

        if not accept_view.value:
            await interaction.edit_original_response(content = f"Ey yo {user.mention} chickened out lmao.", embed = None, view = None)
            return
        
        player1, player2 = interaction.user, user

        manager = DuelManager(player1, player2, interaction)
        
        await manager.run_game()
        return

    @duel.error
    async def on_duel_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await interaction.channel.send(str(error))
        logging.exception("ERROR ERROR ERROR DOES NOT COMPUTEඞඞඞ")
        
async def setup(bot):
    await bot.add_cog(Duel(bot))