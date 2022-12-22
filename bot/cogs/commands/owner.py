import discord
from discord.ext import commands

import typing

class Owner(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(pass_context = True)
    @commands.is_owner()
    async def sync(
        self, 
        ctx: commands.Context, 
        guilds: commands.Greedy[discord.Object], 
        spec: typing.Optional[typing.Literal["~", "*", "^", "."]] = None
        ) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            elif spec == ".":
                ctx.bot.tree.clear_commands()
                await ctx.bot.tree.sync()
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            print(guild.id)
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

async def setup(bot) -> None:
    await bot.add_cog(Owner(bot))