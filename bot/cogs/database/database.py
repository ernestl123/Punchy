class Database():

    def __init__(self, bot) -> None:
        self.bot = bot
        self.db_name = "punchy"
        self.db = bot.db

    #Getter helper function
    async def get_data(self, table_name : str, data_name : str, id : int):
        #Attempt to retrive data from record. val is a Record object(dict/tuple hybrid)
        values = await self.db.fetchrow(f"SELECT {id}, {data_name} FROM {table_name} WHERE id = {id}")

        #If id does not exist in record
        if not values:
            await self.db.execute(f'''
                INSERT INTO {table_name}(id) VALUES ($1)
            ''', id)
            return await self.db.fetchval(f"SELECT {data_name} FROM {table_name} WHERE id = {id}")

        return values[data_name.lower()]
    
    #Set helper function
    async def update_data(self, table_name : str, data_name : str, id : int, new_data) -> None:
        #Ensure that record exists in database
        await self.get_data(table_name, data_name, id)
        
        await self.db.execute(f'''
            UPDATE {table_name} SET {data_name} = $1 where id = {id}
        ''', new_data)

async def setup(bot):
    await bot.add_cog(Database(bot))