from operator import truediv
import discord
from discord.ui import View
from util.dropdown import VoteDrop

class ActionView(View):
    def __init__(self, users, timeout = 60) -> None:
        super().__init__(timeout=timeout)
        self.users_moves = {
            users[0] : [],
            users[1] : []
        }

    async def interaction_check(self, interaction) -> bool:
        user = interaction.user
        await interaction.response.defer()
        if user in self.used_users:
            await interaction.followup.send("You've already clicked on this button!", ephemeral=True)
            return False

        if user in list(self.currentP.keys()) and self.currentP[user].alive and not self.currentP[user].name in self.NONDMROLES:
            self.used_users.append(user)
            return True
        
        if user in list(self.currentP.keys()) and self.currentP[user].name == "isekai" and not self.currentP[user].alive:
            self.used_users.append(user)
            return True
        
        await interaction.followup.send("Ey yo hold up. You don't have an action available tonight get out of here.", ephemeral=True)
        return False

    @discord.ui.button(label='Action', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        role = self.currentP[user]
        #Just makes the prompt. Too lazy to change name
        await role.sendPrompt(self.currentP, self.timeout)
        if not role.embed or not role.view:
            return
        self.view_list.append(role.view)
        await interaction.followup.send(embed = role.embed, view = role.view, ephemeral=True)
    
    def stop(self):
        for view in self.view_list:
            if view:
                view.stop()

        super().stop()

class VoteView(View):
    def __init__(self, vote_dict, nomin_dict, channel, timeout = 180):
        super().__init__(timeout=timeout)
        self.vote_dict = vote_dict
        self.channel = channel
        self.used_users = []

        self.view_dict = {}
        self.nomin_dict = nomin_dict

    async def interaction_check(self, interaction) -> bool:
        user = interaction.user
        await interaction.response.defer()
        if user in self.used_users:
            return False

        if user in list(self.vote_dict):
            self.used_users.append(user)
            return True
        
        await interaction.followup.send("Ey yo hold up. You don't have a say in this democracy. Get out of here.", ephemeral=True)
        return False
    
    @discord.ui.button(label='Vote', style=discord.ButtonStyle.green)
    async def open(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        embed = discord.Embed(
                title = "Nominate for who will be put on trial today!",
                description = "Press the Lock button to lock in your vote! Everyone can see you lock in!",
                colour = discord.Colour.blurple()
            )
        view = VoteDrop(list(self.vote_dict.keys()), user, self.timeout, self.channel)
        await interaction.followup.send(embed = embed, view = view, ephemeral=True)
        self.view_dict[user] = view

    async def tally(self, currentP):
        for voter, view in list(self.view_dict.items()):
            if not view.is_finished():
                if view.get_val():
                    await view.author.send(
                        embed = discord.Embed(title = f"Time's up! You didn't lock in so I'm just going to use what you were hovering on. You have nominated {view.get_val()}."))
                else:
                    await view.author.send(embed = discord.Embed(title = f"Time's up! You didn't nominate anyone. Oh well."))
        
            target = view.get_val()
            if target:
                role_obj = currentP[voter]
                if not role_obj.vote_value:
                    continue

                self.vote_dict[target] += role_obj.vote_value

                if not self.nomin_dict[target]:
                    self.nomin_dict[target] = [voter]
                else:
                    self.nomin_dict[target].append(voter)
                    
        return self.nomin_dict
    
    def stop(self):
        for view in self.view_dict.values():
            if view:
                view.stop()
        super().stop()