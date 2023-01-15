import discord
from discord import app_commands
from discord.ext import commands

import logging

from bot.duel_helpers.duel_manager import DuelManager
from bot.util.accept_view import AcceptView

class Duel(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.duel_users = set()
    
    def check_bot(interaction: discord.Interaction) -> bool:
        return interaction.user

    @app_commands.command(name = "duel", description = "Challenge another player to a duel!")
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def duel(self, interaction: discord.Interaction, user: discord.Member):
        if user.bot:
            await interaction.response.send_message("You can't challenge a bot! You'll definetly lose!", ephemeral=True)
            return
        player1, player2 = interaction.user, user

        if player1 in self.duel_users:
            await interaction.response.send_message("You're currently participating in another duel!", ephemeral=True)
            return
        
        if player2 in self.duel_users:
            await interaction.response.send_message(f"{player2.mention} is currently in a duel!", ephemeral=True)
            return

        self.duel_users.add(player1)
        self.duel_users.add(player2)
        accept_view = AcceptView(user)
        embed = discord.Embed(description=f"{player2.mention}, {player1.mention} has challenged you to an honorable duel. Do you accept?")

        await interaction.response.send_message(embed = embed, view=accept_view)

        await accept_view.wait()

        if not accept_view.value:
            await interaction.edit_original_response(content = f"Ey yo {player2.mention} chickened out lmao.", embed = None, view = None)
            self.duel_users.remove(player1)
            self.duel_users.remove(player2)
            return

        manager = DuelManager(player1, player2, interaction)
        
        try:
            await manager.run_game()  
        except Exception as e:
            raise Exception(e)
        finally:
            self.duel_users.remove(player1)
            self.duel_users.remove(player2)
        
        return

    @duel.error
    async def on_duel_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            return;
        embed = discord.Embed(
            title = f"💀❌An error has occured with command `duel` used by `{interaction.user}`",
            description=str(error),
            color=discord.Colour.brand_red()
        )

        await interaction.channel.send(embed = embed)
        logging.exception("ERROR ERROR ERROR DOES NOT COMPUTEඞඞඞ")

        
async def setup(bot):
    await bot.add_cog(Duel(bot))