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
    
    #Bot check function for commands
    def check_bot(interaction: discord.Interaction) -> bool:
        return interaction.user

    @app_commands.command(name = "duel", description = "Challenge another player to a duel!")
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def duel(self, interaction: discord.Interaction, user: discord.Member):
        #If selected user is a bot
        if user.bot:
            await interaction.response.send_message("You can't challenge a bot! You'll definetly lose!", ephemeral=True)
            return
        
        player1, player2 = interaction.user, user
        
        if player1 == player2:
            await interaction.response.send_message("You can't duel yourself bruh...", ephemeral=True)
            return
        
        #If command user is in a duel
        if player1 in self.duel_users:
            await interaction.response.send_message("You're currently participating in another duel!", ephemeral=True)
            return
        #If selected user is in a duel
        if player2 in self.duel_users:
            await interaction.response.send_message(f"{player2.mention} is currently in a duel!", ephemeral=True)
            return

        #Start duel
        self.duel_users.add(player1)
        self.duel_users.add(player2)

        try:
            accept_view = AcceptView(user)
            embed = discord.Embed(description=f"**{player2.nick if player2.nick else player2.name}**, you have been\nchallenged to a noble duel⚔️!\nDo you accept?", colour = discord.Colour.blurple())
            embed.set_author(name = f"Challenged by: {player1.nick if player1.nick else player1.name}", icon_url = player1.avatar)
            embed.set_thumbnail(url = player2.avatar)

            embed.set_image(url = "https://i.imgflip.com/2sqzch.png?a466656")
            await interaction.response.send_message(embed = embed, view=accept_view)

            await accept_view.wait()

            if not accept_view.value:
                await interaction.edit_original_response(content = f"Ey yo {player2.mention} chickened out of a duel lmao.🐔🐔🐔", embed = None, view = None)
                self.duel_users.remove(player1)
                self.duel_users.remove(player2)
                return

            manager = DuelManager(player1, player2, interaction, self.bot)
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