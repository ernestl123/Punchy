import discord
from discord import app_commands
from discord.ext import commands

from bot.util.action_view import ActionView

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

        player1_name = player1.nick if player1.nick else player1.name
        player2_name = player2.nick if player2.nick else player2.name

        embed = discord.Embed(colour = discord.Colour.greyple())
        embed.set_footer(text = f"{player1_name}, {player2_name} please pick your combination")
        embed.add_field(name = player1_name, value = "___", inline = False)
        embed.add_field(name = player2_name, value = "___", inline = False)
        embed.set_author(name=f"{player1_name} 🆚 {player2_name}")
        await interaction.response.send_message(embed = embed, view=ActionView(player1, player2, embed))
        return

    @duel.error
    async def on_duel_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await interaction.channel.send(str(error))

async def setup(bot):
    await bot.add_cog(Duel(bot))