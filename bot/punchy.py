import discord
from discord.ext import commands

import os
import logging
import logging.handlers
import json
import asyncpg

from bot.cogs.database.data_helpers import UserData, UserRecords

class Punchy(commands.AutoShardedBot):
    DB_NAME = "punchy"
    def __init__(self, command_prefix = commands.when_mentioned, **kwargs) -> None:
        super().__init__(command_prefix=command_prefix, activity=discord.Game(name="/help", type=1), **kwargs)

    def get_cred(self) -> dict:
        #Login credentials stored in secret file
        with open("secret.json", "r") as f:
            secret = json.load(f)
        
        return {
            "user": secret["pg_user"], 
            "password": secret["pg_pw"], 
            "database":self.DB_NAME, 
            "host": "localhost"
        }

    async def start(self, token : str):
        async with self, \
            asyncpg.create_pool(min_size = 2, max_size = 2, **self.get_cred()) as db_pool:
            self.db = db_pool

            self.user_data = UserData(self)
            self.user_records = UserRecords(self)

            logging.basicConfig(filename='discord.log', encoding='utf-8', level=logging.INFO, filemode="w")
            logging.info(f"Established DB connection to database: {self.DB_NAME}!")


            for filename in os.listdir("../Punchy/bot/cogs/commands"):
                if not filename.endswith(".py"):
                    continue
                try:
                    await self.load_extension("bot.cogs.commands." + filename.replace(".py", ""))
                    logging.info("Loading in cog: " + filename.replace(".py", ""))
                except:
                    logging.exception("ERROR ERROR ERROR DOES NOT COMPUTEඞඞඞ")

            await super().start(token)
    
    async def on_ready(self):
        logging.info("Punchy is up and ready to roll!")
        print("Punchy is up and ready to roll!")