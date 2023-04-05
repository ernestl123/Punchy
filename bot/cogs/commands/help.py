import discord
from discord import app_commands
from discord.ext import commands

IMAGE = discord.File("bot/cogs/images/move-diagram.png", filename = "move-diagram.png")
EMBED = discord.Embed(
    title = "📚How to play duel!",
    description = """
    1) Each player starts off with 100♥️. \n
    2) Every round, each player build their combos by selecting **three** moves👊.\n
    3) The results are shown, repeat until a player's HP falls to 0💀.
    
    📕*Move Options*📕
    """,
    color = discord.Colour.blurple()
)
EMBED.add_field(name = "👆Light Attack", value = "Deals small baby damage. Beats 🥊**Heavy Attack**.", inline=False)
EMBED.add_field(name = "🥊Heavy Attack", value = "Deals big boi damage. Beats 🛡️**Block**.", inline=False)
EMBED.add_field(name = "🛡️Block", value = "If successful, the opponent's next attack in the round is nullified. Beats 👆**Light Attack**.", inline=False)
EMBED.set_image(url = "attachment://move-diagram.png")
EMBED.set_footer(text = "Behold my amazing diagram that I drew by hand (if you can believe that)")

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name = "help", description = "How to play duel!")
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def help(self, interaction: discord.Interaction):
        await interaction.response.send_message(file = IMAGE, embed = EMBED)
        return
    
    @app_commands.command(name = "info", description = "Some info about the bot itself")
    async def info(self, interaction : discord.Interaction):
        embed = discord.Embed(description= f'''
            Ping: `{self.bot.latency}`
            Server count: `{len(self.bot.guilds)}`
        ''')
        embed.set_author(name = "Punchy", icon_url = self.bot.user.avatar)
        await interaction.response.send_message(embed = embed)
    
async def setup(bot) -> None:
    await bot.add_cog(Help(bot))