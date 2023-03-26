import asyncpg
import asyncio
import json

#Not part of bot code

async def yes():    
    with open("secret.json", "r") as f:
        secret = json.load(f)

    credentials = {"user": secret["pg_user"], "password": secret["pg_pw"], "database":"punchy", "host": "localhost"}
    db = await asyncpg.create_pool(**credentials)
    print("Established Connection to Punchy database!")

    # await pool.execute('''
    #     CREATE DATABASE punchy
    # ''')
    # await db.execute('''
    #     CREATE TABLE UserInfo (
    #         UserID bigint NOT NULL,
    #         WinsTotal int DEFAULT 0,
    #         GamesTotal int DEFAULT 0,
    #         UniqueWins int DEFAULT 0,
    #         UniqueOpponents bigint[] DEFAULT {},
    #         ForefeitCount int DEFAULT 0
    #     ); 
    # ''')
    print("Created UserInfo table successfully!")
    # await db.execute('''
    #     CREATE TABLE UserRecord (
    #         UserID bigint NOT NULL,
    #         LightCount int DEFAULT 0,
    #         HeavyCount int DEFAULT 0,
    #         BlockCount int DEFAULT 0
    #         Achievements int[] DEFAULT {}
    #     ); 
    # ''')
    print("Created UserRecord table successfully!")
asyncio.get_event_loop().run_until_complete(yes())

