import discord
from discord.ui import View
import traceback

class ActionView(View):
    def __init__(self, 
        player1, player2, 
        embed : discord.Embed, 
        player_obj_dict : dict,
        timeout = 60
        ) -> None:
        super().__init__(timeout=timeout)
        self.player1 = player1
        self.player2 = player2
        self.embed = embed
        
        self.player_obj_dict = player_obj_dict

        #For embed field ID's
        self.users_to_id = {
            self.player1 : 0,
            self.player2 : 1
        }

    async def interaction_check(self, interaction) -> bool:
        user = interaction.user

        #If user is not one of the two playing
        if not user in self.player_obj_dict.keys():
            return False

        #If user already selected all choices
        if len(self.player_obj_dict[user].moves) > 2:
            return False

        return True

    @discord.ui.button(label='Light Attack', emoji='👆', style=discord.ButtonStyle.blurple)
    async def light_button(self, interaction: discord.Interaction, _) -> None:
        user = interaction.user
        self.player_obj_dict[user].add_light()
        
        await self.update_embed(interaction)

    @discord.ui.button(label='Heavy Attack', emoji='🥊', style=discord.ButtonStyle.red)
    async def heavy_button(self, interaction: discord.Interaction, _) -> None:
        user = interaction.user
        self.player_obj_dict[user].add_heavy()
        
        await self.update_embed(interaction)
    
    @discord.ui.button(label='Block', emoji='🛡️', style=discord.ButtonStyle.gray)
    async def block_button(self, interaction: discord.Interaction, _) -> None:
        user = interaction.user
        self.player_obj_dict[user].add_block()

        await self.update_embed(interaction)
    
    def check_finished(self) -> None:
        for player in self.player_obj_dict.values():
            if len(player.moves) < 3:
                return

        self.stop()
        return
    
    async def update_embed(self, interaction: discord.Interaction) -> None:
        field_id = self.users_to_id[interaction.user]
        original_field = self.embed.fields[field_id]
        moves_len = len(self.player_obj_dict[interaction.user].moves)
        self.embed.set_field_at(
            index=field_id, 
            name = original_field.name,
            value="❓" * moves_len + "_" * (3 - moves_len)
        )

        await interaction.response.edit_message(embed = self.embed, view=self)
        self.check_finished()
    
    async def on_error(self, interaction: discord.Interaction, error: Exception, item, /) -> None:
        traceback.print_exc()
        return await super().on_error(interaction, error, item)
