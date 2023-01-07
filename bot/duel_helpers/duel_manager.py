import discord
import asyncio

from bot.util.action_view import ActionView
from bot.duel_helpers.duel_moves.basic_moves import *

class DuelManager:
    #Runs the duel match until either side loses(gets to 0 hp)
    def __init__(self, player1 : discord.User, player2: discord.User, interaction) -> None:
        
        self.player1 = player1
        self.player2 = player2

        player1_name = player1.nick if player1.nick else player1.name
        player2_name = player2.nick if player2.nick else player2.name

        #Display embed for when players are choosing moves
        self.choices_embed = discord.Embed(colour = discord.Colour.greyple())
        self.choices_embed.set_footer(text = f"{player1_name}, {player2_name} please pick your combination")
        self.choices_embed.add_field(name = player1_name, value = "___", inline = False)
        self.choices_embed.add_field(name = player2_name, value = "___", inline = False)
        self.choices_embed.set_author(name=f"{player1_name} 🆚 {player2_name}")
        
        self.interaction = interaction

        self.players_info_dict = {
            player1 : {"health" : 100, "moves" : list()}, 
            player2 : {"health" : 100, "moves" : list()}
            }

    async def run_game(self) -> None:
        action_view = ActionView(self.player1, self.player2, self.choices_embed, self.players_info_dict)
        await self.interaction.response.send_message(embed = self.choices_embed, view = action_view)

        #Run the game while both players have health > 0
        while True:
            #Wait for user input
            await action_view.wait()

            #Retrives player inputs and calculate result
            move_dict = action_view.get_moves()

            #Output results by replacing the choices_embed with the new results_embed

            self.players_info_dict[self.player1]["moves"] = move_dict[self.player1]
            self.players_info_dict[self.player2]["moves"] = move_dict[self.player2]

            for x in range(3):
                await self.do_compare()

                
            results_embed = discord.Embed()
            await self.interaction.response.edit_message(embed=results_embed)

            
            #Refreshes action view and replace current embed with the choices_embed
            await asyncio.sleep(5)  
            action_view = ActionView(self.player1, self.player2, self.choices_embed, self.players_info_dict)
            await self.interaction.response.edit_message(embed = self.choices_embed, view= action_view)
            #break
    
    async def do_compare(self):
        p1_move = self.players_info_dict[self.player1]["moves"].pop()
        p2_move = self.players_info_dict[self.player2]["moves"].pop()

        if p1_move == p2_move:
            return
        
        if p1_move.lose_against(p2_move):
            p2_move.execute(player_info_dict = self.players_info_dict, receiver= self.player1)
            return
        
        if p2_move.lose_against(p1_move):
            p1_move.execute(player_info_dict = self.players_info_dict, receiver = self.player2)
            return
        

