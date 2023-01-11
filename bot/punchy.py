import discord
from discord.ext import commands

import os
import logging
import logging.handlers

class Punchy(commands.AutoShardedBot):
    def __init__(self, command_prefix = commands.when_mentioned, **kwargs) -> None:
        super().__init__(command_prefix=command_prefix, **kwargs)

    async def start(self, token : str):
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO, filemode="w")

        for filename in os.listdir("../Punchy/bot/cogs/commands"):
            if not filename.endswith(".py"):
                continue
            try:
                await self.load_extension("bot.cogs.commands." + filename.replace(".py", ""))
                logging.info("Loading in cog: " + filename.replace(".py", ""))
            except:
                logging.exception("ERROR ERROR ERROR DOES NOT COMPUTE")

        print("Punchy is up and ready to roll!")
        await super().start(token)