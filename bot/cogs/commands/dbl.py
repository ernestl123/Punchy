import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
import topgg

class DBL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not self.bot.testing:
            self.update_stats.start()

    @tasks.loop(minutes=30)
    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count."""
        try:
            await self.bot.topggpy.post_guild_count()
            print(f"Posted server count ({self.bot.topggpy.guild_count})")
        except Exception as e:
            print(f"Failed to post server count\n{e.__class__.__name__}: {e}")

    @update_stats.before_loop
    async def before_update_stats(self):
        await self.bot.wait_until_ready()
    
async def setup(bot) -> None:
    await bot.add_cog(DBL(bot))