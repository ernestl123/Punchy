import discord
from discord import app_commands
from discord.ext import commands

EMBED = discord.Embed(
    title = "📚How to play duel!",
    description = "Insert instructions here",
    color = discord.Colour.blurple()
)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @app_commands.command(name = "help", description = "How to play duel!")
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def help(self, interaction: discord.Interaction):

        await interaction.response.send_message(embed = EMBED, ephemeral=True)
        return

async def setup(bot) -> None:
    await bot.add_cog(Help(bot))