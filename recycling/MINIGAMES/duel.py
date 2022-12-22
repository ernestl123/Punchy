import discord
from discord.ext import commands
import asyncio
import os
import json
import random
import traceback
import MINIGAMES.duel_obj as duel_obj
class Duel(commands.Cog):
    currentPlaying = []

    nothingUrl = ["https://thumbs.gfycat.com/PassionateRectangularBrahmancow-small.gif", "https://media.tenor.com/images/eb84105a1eb998307819b358ac485528/tenor.gif", "https://media0.giphy.com/media/tXL4FHPSnVJ0A/giphy.gif", 
    "https://media0.giphy.com/media/l2JhpjWPccQhsAMfu/giphy.gif",
    "https://i.kym-cdn.com/photos/images/newsfeed/001/057/927/eac.gif",
    "https://thumbs.gfycat.com/BogusFarawayBream-max-1mb.gif"
    ]
    def __init__(self, bot):
        self.bot = bot
        with open("MINIGAMES/duel_message.json", 'r') as f:
            self.move_dict = json.load(f)

    @commands.command(pass_context = True)
    async def duel(self, ctx, victim: discord.Member):
        channel = ctx.channel
        player1 = ctx.author
        if victim.bot:
            await channel.send("You can't challenge a bot. You'll definitely lose!")
        elif victim in self.currentPlaying:
            await channel.send("{} is currently in a duel!".format(victim.name))
        elif player1 in self.currentPlaying:
            await channel.send("{} is currently in a duel!".format(player1.name))
        elif victim != player1:
            try:
                if victim.id == 335430609860296705:
                    challenge = discord.Embed(title = "Oh {}, {} dares to approach you? Is he worthy?".format(victim.name, player1.name), description = "y/n", colour = discord.Colour.red())
                    challenge.set_image(url = "https://i.kym-cdn.com/entries/icons/original/000/028/775/Screen_Shot_2019-03-06_at_4.32.48_PM.jpg")
                else:
                    challenge = discord.Embed(title = "{}, {} has challenged you to a duel. Do you accept?".format(victim.name, player1.name), description = "y/n", colour = discord.Colour.red())
                    challenge.set_image(url = "https://i.ytimg.com/vi/cb5DITStXlI/maxresdefault.jpg")
                    
                challenge.set_author(name = player1.name, icon_url=player1.avatar_url)
                challenge.set_thumbnail(url = victim.avatar_url)
                msg = await channel.send(embed = challenge)
                await msg.add_reaction("🇾")
                await msg.add_reaction("🇳")
                def check(reaction, reactor):
                    return (str(reaction.emoji) == "🇾" or str(reaction.emoji) == "🇳") and reactor == victim 
                try:
                    self.currentPlaying.append(victim)
                    self.currentPlaying.append(player1)
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check)
                    if str(reaction.emoji) == "🇾":
                        await channel.send("Let the duel begin!")
                        await self.playDuel(player1, victim, channel)
                    else:
                        await channel.send("{} declined the duel. Guess someone's too scared.".format(victim.name))
                    
                except asyncio.TimeoutError:
                    await channel.send("The duel request between {} and {} expired.".format(player1.name, victim.name))
                self.currentPlaying.remove(victim)
                self.currentPlaying.remove(player1)
            except discord.errors.Forbidden:
                await ctx.send("Bruh one of you turned off your privacy settings. That's real low...")
                if victim in self.currentPlaying:
                    self.currentPlaying.remove(victim)
                if player1 in self.currentPlaying:
                    self.currentPlaying.remove(player1)
            except:
                print(traceback.format_exc())
                if victim in self.currentPlaying:
                    self.currentPlaying.remove(victim)
                if player1 in self.currentPlaying:
                    self.currentPlaying.remove(player1)
        else:
            await channel.send("You can't challenge yourself dummy.")
    
    async def playDuel(self, player1, player2, channel):
        p1_obj = duel_obj.Dueler(player1, self.bot)
        p2_obj = duel_obj.Dueler(player2, self.bot)
        p1_obj.set_moves(p2_obj, self.move_dict)
        p2_obj.set_moves(p1_obj, self.move_dict)

        await channel.send("{} please check your DM!".format(player1.name))
        while p1_obj.health !=0 and p2_obj.health !=0:

            #Sends prompts to both duelers
            await p1_obj.prompt()
            await p2_obj.prompt()

            if not p1_obj.choice and not p2_obj.choice:
                break

            if not p1_obj.choice and not p2_obj.choice.id == 3:
                await p2_obj.choice.execute(channel)
                continue
                
            if not p2_obj.choice and not p1_obj.choice.id == 3:
                await p1_obj.choice.execute(channel)
                continue
            
            try:
                winning_move = p1_obj.choice.compare(p2_obj.choice)
                if winning_move:
                    await winning_move.execute(channel)
                    continue
            except AttributeError:
                pass
            
            try:
                await channel.send(embed = discord.Embed(title = f"{player1.name} chose a {p1_obj.choice.name}!\n\n{player2.name} chose a {p2_obj.choice.name}!", colour = discord.Colour.gold()))
            except:
                pass

            embed = discord.Embed(title = "Lol nothing happened.", colour = discord.Colour.red())
            embed.set_image(url = random.choice(self.nothingUrl))
            await channel.send(embed = embed)

        if p1_obj.health == 0:
            embed = discord.Embed(title = "{} wins the duel!".format(player2.name), colour = discord.Colour.blue())
            embed.set_thumbnail(url = player2.avatar_url)
        elif p2_obj.health == 0:
            embed = discord.Embed(title ="{} wins the duel!".format(player1.name), colour = discord.Colour.blue())
            embed.set_thumbnail(url = player1.avatar_url)
        else:
            embed = discord.Embed(title = "No contest.")
            embed.set_image(url = "https://thumbs.gfycat.com/FailingFavorableBaleenwhale-size_restricted.gif")
        await channel.send(embed = embed)

        
    
def setup(bot):
    bot.add_cog(Duel(bot))
