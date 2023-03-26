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
    
    #Getter helper function
    async def get_data(self, table_name : str, data_name : str, id : int):
        #Attempt to retrive data from record. val is a Record object(dict/tuple hybrid)
        val = await self.db.fetchval(f"SELECT {data_name} FROM {table_name} WHERE id = {id}")

        #If id does not exist in record
        if not val:
            await self.db.execute(f'''
                INSERT INTO {table_name}(id)
            ''')
            val = await self.db.fetchval(f"SELECT {data_name} FROM {table_name} WHERE id = {id}")
        
        return val
    
    #Set helper function
    async def update_data(self, table_name : str, data_name : str, id : int, new_data) -> None:
        #Ensure that record exists in database
        await self.get_data(table_name, data_name, id)
        
        await self.db.execute(f'''
            UPDATE {table_name} SET {data_name} = $1 where id = {id}
        ''', new_data)

    async def get_wins_total(self, user_id : int) -> int:
        return await self.get_data("UserInfo", "WinsTotal", user_id)
    
    async def get_games_total(self, user_id : int) -> int:
        return await self.get_data("UserInfo", "WinsTotal", user_id)
    
    async def get_wins_unique(self, user_id : int) -> int:
        return await self.get_data("UserInfo", "UniqueWins", user_id)
    
    async def get_games_total(self, user_id : int) -> list:
        return await self.get_data("UserInfo", "UniqueOpponents", user_id)
    
    async def get_forfeit_count(self, user_id : int) -> list:
        return await self.get_data("UserInfo", "ForfeitCount", user_id)
    
    #Get all record columns from UserInfo table of a specific user
    async def get_user(self, user_id : int) -> dict:
        await self.get_wins_total(user_id)
        return dict(await self.db.fetchrow(f"SELECT * FROM UserInfo WHERE id = {id}"))

async def setup(bot):
    await bot.add_cog(Database(bot))