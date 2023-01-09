import discord
import asyncio

from bot.util.action_view import ActionView
from bot.duel_helpers.duel_moves.basic_moves import *

class DuelManager:
    #Runs the duel match until either side loses(gets to 0 hp)
    def __init__(self, player1 : discord.User, player2: discord.User, interaction) -> None:
        
        self.player1 = player1
        self.player2 = player2

        self.player1_name = player1.nick if player1.nick else player1.name
        self.player2_name = player2.nick if player2.nick else player2.name

        self.players_info_dict = {
            player1 : {"health" : 100, "moves" : list()}, 
            player2 : {"health" : 100, "moves" : list()}
        }

        #Display embed for when players are choosing moves
        self.choices_embed = discord.Embed(colour = discord.Colour.greyple(), description=self.make_health_str())
        self.choices_embed.set_footer(text = f"{self.player1_name}, {self.player2_name} please pick your combination")
        self.choices_embed.add_field(name = self.player1_name, value = "___")
        self.choices_embed.add_field(name = self.player2_name, value = "___")
        self.choices_embed.set_author(name=f"{self.player1_name} 🆚 {self.player2_name}")
        
        self.interaction = interaction

    async def run_game(self) -> None:
        action_view = ActionView(self.player1, self.player2, self.choices_embed, self.players_info_dict)
        await self.interaction.response.send_message(embed = self.choices_embed, view = action_view)

        #Run the game while both players have health > 0
        #TODO: Add break statement when game finishes
        while True:
            #Wait for user input
            await action_view.wait()

            #Retrives player inputs and calculate result
            move_dict = action_view.get_moves()

            #Output results by replacing the choices_embed with the new results_embed

            self.players_info_dict[self.player1]["moves"] = move_dict[self.player1]
            self.players_info_dict[self.player2]["moves"] = move_dict[self.player2]

            results_embed = discord.Embed(title = "Results:", description=self.make_health_str())
            
            for x in range(3):
                embed_field_value, versus_str = await self.do_compare()
                results_embed.description = self.make_health_str()
                results_embed.add_field(name= f"Round {x} - {versus_str}", value= embed_field_value, inline=False)
                await self.interaction.edit_original_response(embed=results_embed)
                await asyncio.sleep(3)
            
            await self.interaction.edit_original_response(embed=results_embed)

            
            #Refreshes action view and replace current embed with the choices_embed
            await asyncio.sleep(5)

            #Clears slected moves from last round
            self.players_info_dict[self.player1]["moves"] = []
            self.players_info_dict[self.player2]["moves"] = []
            self.choices_embed.clear_fields()
            self.choices_embed.add_field(name = self.player1_name, value = "___")
            self.choices_embed.add_field(name = self.player2_name, value = "___")
            self.choices_embed.description = self.make_health_str()

            action_view = ActionView(self.player1, self.player2, self.choices_embed, self.players_info_dict)
            await self.interaction.edit_original_response(embed = self.choices_embed, view= action_view)
            #break
    
    async def do_compare(self) -> tuple:
        p1_move = self.players_info_dict[self.player1]["moves"].pop()
        p2_move = self.players_info_dict[self.player2]["moves"].pop()
        versus_str = f"{p1_move} vs {p2_move}"
        if p1_move == p2_move:
            return "Nothing happened...", versus_str
        
        if p1_move.lose_against(p2_move):
            return p2_move.execute(player_info_dict = self.players_info_dict, receiver= self.player1, attacker = self.player2), versus_str
            
        if p2_move.lose_against(p1_move):
            return p1_move.execute(player_info_dict = self.players_info_dict, receiver = self.player2, attacker = self.player1), versus_str
    
    def make_health_str(self):
        player1_str = f"{self.player1_name}\n{self.make_health_bar(self.player1)}💙"
        player2_str = f"{self.player2_name}\n{self.make_health_bar(self.player2)}❤️"
        return player1_str + "\n\n" + player2_str
            
    def make_health_bar(self, user : discord.User) -> str:
        health = self.players_info_dict[user]["health"]

        max_health = 100
        max_bars = 20

        dash_convert = int(max_health/max_bars)
        health_display = "=" * int(health/dash_convert)
        missing_health_display = "-" * (max_bars - int(health/dash_convert))
        return "|" + health_display + f"| {health}"
