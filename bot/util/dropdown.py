from time import time
import discord
from discord.ext import commands
from util.option import Confirm

# Defines a custom Select containing colour options
# that the user can choose. The callback function
# of this class is called when the user changes their choice
class OneTargetSelect(discord.ui.Select):
    def __init__(self, options : list):
        super().__init__(placeholder='Choose your target...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        self.placeholder = self.values[0]
        await interaction.response.edit_message(view = self.view)
        #await interaction.response.send_message(f'Your have selected {self.values[0]}', ephemeral = True)
    
    def get_val(self, user_list):
        if not self.values:
            return None
        for user in user_list:
            if str(user) in self.values[0]:
                return user

class TwoTargetSelect(discord.ui.Select):
    def __init__(self, options : list):
        super().__init__(placeholder='Choose TWO targets...', min_values=2, max_values=2, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        await interaction.response.send_message(f'Your choices are {self.values[0]} and {self.values[1]}', ephemeral= True)
    
    def get_val(self, user_list):
        if len(self.values) < 2:
            return None

        if not self.values[0] or not self.values[1]:
            return None

        target1 = None
        target2 = None
        for user in user_list:
            if str(user) in self.values[0]:
                target1 = user
            elif str(user) in self.values[1]:
                target2 = user

        if not self.values[0] or not self.values[1]:
            return None

        return [target1, target2]

class DropDownConfirm(discord.ui.View):
    def __init__(self, players, timeout):
        super().__init__()
        self.timeout = timeout
        self.options = [discord.SelectOption(label = "N/A", description = "Select nothing")]
        self.message = None
        for user in players:
            try:
                if user.nick:
                    descr = user.nick
                else:
                    descr = user.name
            except:
                descr = user
                
            self.options.append(discord.SelectOption(label = f"{user}", description = descr))
    
    @discord.ui.button(label='Lock in', style=discord.ButtonStyle.green, emoji='🔒')
    async def lock(self, interaction: discord.Interaction, button: discord.ui.Button):
        #await interaction.response.send_message(f"You have locked in your choice: {self.options[0]}")
        for child in self.children:
            child.disabled = True
            
        self.stop()
        return await interaction.response.edit_message(view=self)
    
    def get_val(self, user_list):
        val = self.children[1].get_val(user_list)
        return None if val == "N/A" else val
        
class OneOptionDrop(DropDownConfirm):
    def __init__(self, players : list, timeout):
        super().__init__(players, timeout)
        self.timeout = timeout

        self.add_item(OneTargetSelect(self.options))

class TwoOptionDrop(DropDownConfirm):
    def __init__(self, players : list, timeout):
        super().__init__(players, timeout)

        self.add_item(TwoTargetSelect(self.options))

class VoteDrop(discord.ui.View):
    def __init__(self, players, author, timeout, channel):
        super().__init__()
        self.timeout = timeout
        self.options = [discord.SelectOption(label = "N/A", description = "Select nothing")]
        self.channel = channel
        self.players = players
        self.author = author
        for user in players:
            if user.nick:
                descr = user.nick
            else:
                descr = user.name
            self.options.append(discord.SelectOption(label = f"{user}", description = descr))
        self.add_item(OneTargetSelect(self.options))
    
    @discord.ui.button(label='Lock in', style=discord.ButtonStyle.green, emoji='🔒')
    async def lock(self, interaction: discord.Interaction, button: discord.ui.Button):
        #await interaction.response.send_message(f"You have locked in your choice: {self.options[0]}")
        for child in self.children:
            child.disabled = True
        victim = self.get_val()
        self.stop()
        embed = discord.Embed(colour=discord.Colour.green())
        if not victim:
            #embed.set_thumbnail(url = victim.avatar)
            victim = "no one"

        embed.set_author(name = self.author.name, icon_url = self.author.avatar)
        embed.description = f"‼️A vote has been casted by {self.author.mention}!"
        embed.set_footer(text = f"Note that this could also mean {self.author} voted no one!")
        await self.channel.send(embed = embed)
        return await interaction.response.edit_message(view=self)
    
    def get_val(self):
        val = self.children[1].get_val(self.players)
        return None if val == "N/A" else val
