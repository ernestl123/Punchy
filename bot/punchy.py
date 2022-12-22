import discord
from discord.ext import commands

import os
import typing

class Punchy(commands.AutoShardedBot):
    def __init__(self, command_prefix = commands.when_mentioned, **kwargs) -> None:
        super().__init__(command_prefix=command_prefix, **kwargs)

    async def start(self, token : str):
        for filename in os.listdir("../Punchy/bot/cogs/commands"):
            if not filename.endswith(".py"):
                continue
            try:
                await self.load_extension("bot.cogs.commands." + filename.replace(".py", ""))
            except Exception as e:
                print(str(e))
            print(filename.replace(".py", ""))

        await super().start(token)