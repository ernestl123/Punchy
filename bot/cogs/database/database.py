import discord
from discord.ext import commands
import asyncio
import asyncpg
import json

class Database(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
        self.db_name = "punchy"
    
    async def connect_db(self):
        #Login credentials stored in secret file
        with open("secret.json", "r") as f:
            secret = json.load(f)
        
        credentials = {"user": secret["pg_user"], "password": secret["pg_pw"], "database":self.db_name, "host": "localhost"}
        
        #Connect to database
        self.db = await asyncpg.create_pool(min_size = 2, max_size = 2, **credentials)
        print(f"Established DB connection to database: {self.db_name}!")