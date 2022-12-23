import discord
from discord.ui import View

class ActionView(View):
    def __init__(self, player1, player2, embed : discord.Embed, timeout = 60) -> None:
        super().__init__(timeout=timeout)
        self.users_moves = {
            player1 : [],
            player2 : []
        }

        self.player_to_id = {
            player1 : 0,
            player2 : 1
        }

        self.embed = embed

    async def interaction_check(self, interaction) -> bool:
        user = interaction.user

        #If user is not one of the two playing
        if not user in self.users_moves.keys():
            return False

        #If user already selected all choices
        if len(self.users_moves[user]) > 2:
            return False

        return True

    @discord.ui.button(label='Light Attack', emoji='👆', style=discord.ButtonStyle.blurple)
    async def light_button(self, interaction: discord.Interaction, _):
        print("light")
        user = interaction.user
        self.users_moves[user].append('L')
        
        await self.update_embed(interaction)

    @discord.ui.button(label='Heavy Attack', emoji='🥊', style=discord.ButtonStyle.red)
    async def heavy_button(self, interaction: discord.Interaction, _):
        print("heavy")
        user = interaction.user
        self.users_moves[user].append('H')
        
        await self.update_embed(interaction)
    
    @discord.ui.button(label='Block', emoji='🛡️', style=discord.ButtonStyle.gray)
    async def block_button(self, interaction: discord.Interaction, _):
        print("block")
        user = interaction.user
        self.users_moves[user].append('B')

        await self.update_embed(interaction)
    
    def check_finished(self):
        for moveset in self.users_moves.values():
            if len(moveset) < 3:
                return

        self.stop()
        return
    
    async def update_embed(self, interaction: discord.Interaction):
        field_id = self.player_to_id[interaction.user]
        original_field = self.embed.fields[field_id]
        self.embed.set_field_at(
            index=field_id, 
            name = original_field.name,
            value="❓" * len(self.users_moves[interaction.user]) + "_" * (3 - len(self.users_moves[interaction.user]))
        )

        await interaction.response.edit_message(embed = self.embed, view=self)
        self.check_finished()
