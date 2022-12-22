from discord.ext import commands

import discord

# Define a simple View that gives us a confirmation menu
class Confirm(discord.ui.View):
    def __init__(self, confirm_str, cancel_str, user):
        super().__init__()
        self.value = None
        self.confirm_str = confirm_str
        self.cancel_str = cancel_str
        self.user = user
        self.timeout = 60
    
    async def interaction_check(self, interaction) -> bool:
        return interaction.user == self.user

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.confirm_str, ephemeral=True)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.cancel_str, ephemeral=True)
        self.value = False
        self.stop()

class DuelChoice(discord.ui.View):
    def __init__(self, user):
        super().__init__()
        self.value = None
        self.timeout = 15
        self.user = user

    async def interaction_check(self, interaction) -> bool:
        return interaction.user == self.user

    @discord.ui.button(label='Light Attack', style=discord.ButtonStyle.blurple, emoji="👊")
    async def light(self, interaction: discord.Interaction, button: discord.ui.Button):
        #await interaction.response.send_message("You have chosen Light Attack. Please return to the channel.", ephemeral=True)
        await interaction.response.edit_message()
        self.value = 'A'
        button.style = discord.ButtonStyle.gray
        self.stop()

    @discord.ui.button(label='Heavy Attack', style=discord.ButtonStyle.red, emoji="🪓")
    async def heavy(self, interaction: discord.Interaction, button: discord.ui.Button):
        #await interaction.response.send_message("You have chosen Heavy Attack. Please return to the channel.", ephemeral=True)
        await interaction.response.edit_message()
        self.value = 'B'
        button.style = discord.ButtonStyle.gray
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Block', style=discord.ButtonStyle.green, emoji="🛡️")
    async def block(self, interaction: discord.Interaction, button: discord.ui.Button):
        #await interaction.response.send_message("You have chosen Block Attack. Please return to the channel.", ephemeral=True)
        await interaction.response.edit_message()
        self.value = 'C'
        button.style = discord.ButtonStyle.gray
        self.stop()

    @discord.ui.button(label='Forfeit', style=discord.ButtonStyle.grey, emoji="⬜")
    async def forfeit(self, interaction: discord.Interaction, button: discord.ui.Button):
        #await interaction.response.send_message("You chose to forfeit. Please return to the channel", ephemeral=True)
        await interaction.response.edit_message()
        self.value = 'X'
        button.style = discord.ButtonStyle.gray
        self.stop()  

class VoteButtons(discord.ui.View):
    def __init__(self, user_list, currentP, embed):
        super().__init__()
        self.user_list = user_list
        self.voted = []
        self.guilty = []
        self.innocent = []
        self.value = (self.guilty, self.innocent)
        self.timeout = 20
        self.currentP = currentP
        self.embed = embed
    
    async def interaction_check(self, interaction) -> bool:
        return interaction.user in self.user_list

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='GUILTY', style=discord.ButtonStyle.red, emoji="👿")
    async def guilty(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        if user in self.guilty:
            await interaction.response.defer()
            return
        self.guilty.append(user)
        if user in self.voted:
            self.innocent.remove(user)
        else:
            self.voted.append(user)
        self.update_embed()
        await interaction.response.edit_message(embed = self.embed, view=self)
        self.check_voted()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='INNOCENT', style=discord.ButtonStyle.green, emoji = "👼")
    async def innocent(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        if user in self.innocent:
            await interaction.response.defer()
            return
        self.innocent.append(user)
        if user in self.voted:
            self.guilty.remove(user)
        else:
            self.voted.append(user)

        self.update_embed()
        await interaction.response.edit_message(embed = self.embed, view=self)
        self.check_voted()
    
    @discord.ui.button(label='ME NO VOTE', style=discord.ButtonStyle.gray, emoji = "🙅‍♂️")
    async def abstain(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user

        if user in self.guilty:
            self.guilty.remove(user)
        elif user in self.innocent:
            self.innocent.remove(user)

        if user in self.voted:
            self.voted.remove(user)

        self.update_embed()
        await interaction.response.edit_message(embed = self.embed, view=self)
        self.check_voted()

    def check_voted(self):
        if len(self.voted) == len(self.user_list):
            for child in self.children:
                child.disabled = True
            self.stop
    
    def update_embed(self):
        
        guilty_str = str()
        for voter in self.guilty:
            guilty_str += f"🟥{voter.mention}\n"
        innocent_str = str()
        for voter in self.innocent:
            innocent_str += f"⬜{voter.mention}\n"
        
        if not guilty_str:
            guilty_str = "No one..."
        if not innocent_str:
            innocent_str = "No one..."
        self.embed.set_field_at(0, name = f"👿Guilty ({len(self.guilty)})", value = guilty_str)
        self.embed.set_field_at(1, name =  f"Innocent ({len(self.innocent)})", value = innocent_str)
        self.value = (self.guilty, self.innocent)
    
    def get_val(self):
        return self.value

class NominateButtons(discord.ui.View):
    def __init__(self, user_list, embed):
        super().__init__()
        self.user_list = user_list
        self.voted = []
        self.result_dict = {}
        self.timeout = 20
        self.embed = embed

        for user in user_list:
            self.add_item(discord.ui.Button(label=str(user)))
    
    def update_embed(self):
        
        guilty_str = str()
        for voter in self.guilty:
            guilty_str += f"🟥{voter.mention}\n"
        innocent_str = str()
        for voter in self.innocent:
            innocent_str += f"⬜{voter.mention}\n"
        
        if not guilty_str:
            guilty_str = "No one..."
        if not innocent_str:
            innocent_str = "No one..."
        self.embed.set_field_at(0, name = f"👿Guilty ({len(self.guilty)})", value = guilty_str)
        self.embed.set_field_at(1, name =  f"Innocent ({len(self.innocent)})", value = innocent_str)
        self.value = (self.guilty, self.innocent)
    
    def get_val(self):
        return self.value

