import discord
from discord.ext import commands
import asyncio

from bot.punchy import Punchy

async def run_punchy() -> None:
    bot = Punchy(intents = discord.Intents.default())

    async with bot:
        await bot.start("MTA1NTM5Mzg3MTk1MTA0MDU2Mg.GqaHXC.fxxxfFSR4qnYEEZLAYmQTWGlqrXciMn_ch6Djs")

asyncio.run(run_punchy())