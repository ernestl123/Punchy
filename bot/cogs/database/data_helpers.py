from bot.cogs.database.database import Database

class UserData(Database):
    
    async def get_wins_total(self, user_id : int) -> int:
        return await self.get_data("UserInfo", "WinsTotal", user_id)
    
    async def get_games_total(self, user_id : int) -> int:
        return await self.get_data("UserInfo", "GamesTotal", user_id)
    
    async def get_wins_unique(self, user_id : int) -> int:
        return await self.get_data("UserInfo", "UniqueWins", user_id)
    
    async def get_unique_opp(self, user_id : int) -> list:
        val = await self.get_data("UserInfo", "UniqueOpponents", user_id)
        if not val:
            await self.update_data("UserInfo", "UniqueOpponents", user_id, [])
            return []
        
        return val
    
    #Get all record columns from UserInfo table of a specific user
    async def get_user(self, user_id : int) -> dict:
        await self.get_wins_total(user_id)
        return await self.db.fetchrow(f"SELECT * FROM UserInfo WHERE id = {user_id}")

    async def add_win(self, user_id : int, opp_id : int) -> None:
        wins_total = await self.get_wins_total(user_id) + 1
        await self.update_data("UserInfo", "WinsTotal", user_id, wins_total)

        unique_opp_list = await self.get_unique_opp(user_id)
        if not opp_id in unique_opp_list:
            await self.update_data("UserInfo", "UniqueWins", user_id, await self.get_wins_unique(user_id) + 1)
            
            unique_opp_list.append(opp_id)
            await self.update_data("UserInfo", "UniqueOpponents", user_id, unique_opp_list)
    
    async def add_game(self, user_id : int) -> None:
        await self.update_data("UserInfo", "GamesTotal", user_id, await self.get_games_total(user_id) + 1)

class UserRecords(Database):

    async def get_forfeit_count(self, user_id : int) -> int:
        return await self.get_data("UserInfo", "ForfeitCount", user_id)
    
    async def get_light_count(self, user_id : int) -> int:
        return await self.get_data("UserRecord", "LightCount", user_id)
    
    async def get_heavy_count(self, user_id : int) -> int:
        return await self.get_data("UserRecord", "HeavyCount", user_id)
    
    async def get_block_count(self, user_id : int) -> int:
        return await self.get_data("UserRecord", "BlockCount", user_id)
    
    async def get_achievments(self, user_id : int) -> list:
        val = await self.get_data("UserRecord", "Achievements", user_id)
        if not val:
            await self.update_data("UserRecord", "Achievements", user_id, [])
            return []
        
        return val