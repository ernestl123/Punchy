import discord
from discord.ui import View
from bot.duel_helpers.duel_moves.basic_moves import *
import traceback

DEFAULT_MOVES = [LightAttack(), HeavyAttack(), Block()]

class ActionView(View):
    def __init__(self, 
        player1, player2, 
        embed : discord.Embed, 
        player_info_dict : dict,
        player1_moves = DEFAULT_MOVES, 
        player2_moves = DEFAULT_MOVES, 
        timeout = 60
        ) -> None:
        super().__init__(timeout=timeout)
        self.player1 = player1
        self.player2 = player2
        self.embed = embed
        
        self.users_moves = {
            self.player1 : [],
            self.player2 : []
        }
        
        self.users_move_objs = {
            self.player1 : player1_moves,
            self.player2 : player2_moves
        }

        self.users_to_id = {
            self.player1 : 0,
            self.player2 : 1
        }

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
    async def light_button(self, interaction: discord.Interaction, _) -> None:
        user = interaction.user
        self.users_moves[user].append(self.users_move_objs[user][0])
        
        await self.update_embed(interaction)

    @discord.ui.button(label='Heavy Attack', emoji='🥊', style=discord.ButtonStyle.red)
    async def heavy_button(self, interaction: discord.Interaction, _) -> None:
        user = interaction.user
        self.users_moves[user].append(self.users_move_objs[user][1])
        
        await self.update_embed(interaction)
    
    @discord.ui.button(label='Block', emoji='🛡️', style=discord.ButtonStyle.gray)
    async def block_button(self, interaction: discord.Interaction, _) -> None:
        user = interaction.user
        self.users_moves[user].append(self.users_move_objs[user][2])

        await self.update_embed(interaction)
    
    def check_finished(self) -> None:
        for moveset in self.users_moves.values():
            if len(moveset) < 3:
                return

        self.stop()
        return
    
    async def update_embed(self, interaction: discord.Interaction) -> None:
        field_id = self.users_to_id[interaction.user]
        original_field = self.embed.fields[field_id]
        self.embed.set_field_at(
            index=field_id, 
            name = original_field.name,
            value="❓" * len(self.users_moves[interaction.user]) + "_" * (3 - len(self.users_moves[interaction.user]))
        )

        await interaction.response.edit_message(embed = self.embed, view=self)
        self.check_finished()
    
    def get_moves(self) -> tuple:
        #Pad the empty spaces in each move list with DoNothing
        for user, moves in self.users_moves.items():
            if len(moves) < 3:
                moves += [DoNothing() for _ in range(3 - len(moves))]
        return self.users_moves
    
    async def on_error(self, interaction: discord.Interaction, error: Exception, item, /) -> None:
        traceback.print_exc()
        return await super().on_error(interaction, error, item)
