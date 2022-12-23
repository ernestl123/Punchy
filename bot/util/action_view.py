import discord
from discord.ui import View

class ActionView(View):
    def __init__(self, player1, player2, timeout = 60) -> None:
        super().__init__(timeout=timeout)
        self.users_moves = {
            player1 : [],
            player2 : []
        }

    async def interaction_check(self, interaction) -> bool:
        user = interaction.user
        await interaction.response.defer()

        #If user is not one of the two playing
        if not user in self.users_moves.keys():
            return False

        #If user already selected all choices
        if len(self.users_moves[user]) > 2:
            return False

        return True

    @discord.ui.button(label='Light Attack', emoji='👆', style=discord.ButtonStyle.blurple)
    async def light_button(self, interaction: discord.Interaction, _):
        user = interaction.user
        self.users_moves[user].append('L')
        

    @discord.ui.button(label='Heavy Attack', emoji='🥊', style=discord.ButtonStyle.red)
    async def heavy_button(self, interaction: discord.Interaction, _):
        user = interaction.user
        self.users_moves[user].append('H')
    
    @discord.ui.button(label='Block', emoji='🛡️', style=discord.ButtonStyle.gray)
    async def block_button(self, interaction: discord.Interaction, _):
        user = interaction.user
        self.users_moves[user].append('B')