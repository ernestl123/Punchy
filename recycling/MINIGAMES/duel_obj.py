import random
import asyncio
import discord


    
#Move objects 
class light():
    def __init__(self, me_obj, opponent_obj, move_dict):
        self.name = "light attack"
        self.me_obj = me_obj
        self.id = 1
        self.opponent_obj = opponent_obj
        self.move_dict = move_dict

        self.me_name = self.me_obj.user.name
        self.opp_name = self.opponent_obj.user.name
    def compare(self, move):
        if not move:
            return self
            
        if move.id == 3:
            return move
    
        
        if move.id == 1:
            return None
        
        #If opponent's move is 2 or None
        return self
    
    async def execute(self, channel):
        damage = random.randint(10, 20)
        self.opponent_obj.health -= damage
        if self.opponent_obj.health < 0:
            self.opponent_obj.health = 0
        try:
            await channel.send(embed = discord.Embed(title = f"{self.me_name} chose a {self.name}!\n\n{self.opp_name} chose a {self.opponent_obj.choice.name}!", colour = discord.Colour.red()))
        except:
            pass
        random_text = random.choice(list(self.move_dict["light attack"].keys()))
        title_str = random_text.format(self.me_obj.user.name, self.opponent_obj.user.name)
        embed = discord.Embed(
            title = title_str, 
            description = f"**{self.opponent_obj.user.name}** took **{damage}** damage!!\n\n{self.me_obj.user.name} {self.me_obj.health}❤️ vs {self.opponent_obj.user.name} {self.opponent_obj.health}❤️", 
            colour = discord.Colour.red()
            )
        embed.set_image(url = self.move_dict["light attack"][random_text])
        
        await channel.send(embed = embed)

class heavy():
    def __init__(self, me_obj, opponent_obj, move_dict):
        self.name = "heavy attack"
        self.me_obj = me_obj
        self.id = 2
        self.opponent_obj = opponent_obj
        self.move_dict = move_dict

        self.me_name = self.me_obj.user.name
        self.opp_name = self.opponent_obj.user.name
    def compare(self, move):
        if not move:
            return self

        if move.id == 1:
            return move
        
        if move.id == 2:
            return None
        
        #If opponent's move is 3 or None
        return self
    
    async def execute(self, channel):
        damage = random.randint(21, 30)
        self.opponent_obj.health -= damage
        if self.opponent_obj.health < 0:
            self.opponent_obj.health = 0
        
        try:
            await channel.send(embed = discord.Embed(title = f"{self.me_name} chose a {self.name}!\n\n{self.opp_name} chose a {self.opponent_obj.choice.name}!", colour = discord.Colour.red()))
        except:
            pass
        random_text = random.choice(list(self.move_dict["heavy attack"].keys())) 
        title_str = random_text.format(self.me_obj.user.name, self.opponent_obj.user.name)
        embed = discord.Embed(
            title = title_str, 
            description = f"**{self.opponent_obj.user.name}** took **{damage}** damage!!\n\n{self.me_obj.user.name} {self.me_obj.health}❤️ vs {self.opponent_obj.user.name} {self.opponent_obj.health}❤️", 
            colour = discord.Colour.red()
            )
        embed.set_image(url = self.move_dict["heavy attack"][random_text])

        await channel.send(embed = embed)
    
class block():
    def __init__(self, me_obj, opponent_obj, move_dict):
        self.name = "block"
        self.me_obj = me_obj
        self.id = 3
        self.opponent_obj = opponent_obj
        self.move_dict = move_dict

        self.me_name = self.me_obj.user.name
        self.opp_name = self.opponent_obj.user.name
    def compare(self, move):
        if not move:
            return None

        if move.id == 1:
            return self
        
        if move.id == 2:
            return move

        return None

    async def execute(self, channel):
        self.opponent_obj.stunned = True
        try:
            await channel.send(embed = discord.Embed(title = f"{self.me_name} chose a {self.name}!\n\n{self.opp_name} chose a {self.opponent_obj.choice.name}!", colour = discord.Colour.red()))
        except:
            pass
        random_text = random.choice(list(self.move_dict["block"].keys()))
        title_str = random_text.format(self.me_obj.user.name, self.opponent_obj.user.name)
        embed = discord.Embed(
            title = title_str, 
            description = f"**{self.opponent_obj.user.name}** is stunned for one turn!\n\n{self.me_obj.user.name} {self.me_obj.health}❤️ vs {self.opponent_obj.user.name} {self.opponent_obj.health}❤️", 
            colour = discord.Colour.red()
            )
        embed.set_image(url = self.move_dict["block"][random_text])
        await channel.send(embed = embed)
class Dueler:

    #Message prompt for each turn
    EMBED = discord.Embed(title = "Alright fighter, choose your move.", description = "Enter the number associated with your choice.", colour = discord.Colour.red())
    EMBED.add_field(name = "1. Light attack", value = "Beats a heavy attack, but can be blocked.")
    EMBED.add_field(name = "2. Heavy attack", value = "Beats a block, but can be interupted by a light attack.")
    EMBED.add_field(name = "3. Block", value = "Blocks light attack and stuns the opponent, but cannot block heavy attack.")
    EMBED.set_image(url = "https://art.ngfiles.com/images/332000/332918_phatalphd_cowboy-standoff.jpg?f1419452016")

    def __init__(self, user, bot):
        self.user = user
        self.health = 100
        self.choice = None
        self.bot = bot
        self.stunned = False

    def set_moves(self, opponent_obj, move_dict):
        self.MOVESET = [light(self, opponent_obj, move_dict), heavy(self, opponent_obj, move_dict), block(self, opponent_obj, move_dict)]

    async def prompt(self):
        if self.stunned:
            self.choice = None
            self.stunned = False
            return
            
        self.choice = None
        await self.user.send(embed = self.EMBED)
        try:
            answer = await self.bot.wait_for('message', check=lambda message: message.author == self.user and (message.content in ["1", "2", "3"]), timeout = 30)
            self.choice = self.MOVESET[int(answer.content)-1]
            await self.user.send("Got it. Return to the channel.")

        except asyncio.TimeoutError:
            await self.user.send("Boi you afk. You gonna die. Think faster next time.")
            self.choice = None
    
