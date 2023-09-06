import discord
from discord.ext import commands
import asyncio
import json

from bot.punchy import Punchy
testing = False

async def run_punchy() -> None:
    bot = Punchy(intents = discord.Intents.default())

    with open("secret.json", 'r') as f:
        if testing:
            key = json.load(f)["test_key"]
        else:
            key = json.load(f)["key"]
    async with bot:
        await bot.start(key)

asyncio.run(run_punchy())