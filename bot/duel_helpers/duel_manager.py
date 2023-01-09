import discord
import asyncio

from bot.util.action_view import ActionView
from bot.duel_helpers.duel_moves.basic_moves import *
from bot.duel_helpers.player import Player

class DuelManager:
    #Runs the duel match until either side loses(gets to 0 hp)
    def __init__(self, player1 : discord.User, player2: discord.User, interaction) -> None:
        player1_name = player1.nick if player1.nick else player1.name
        player2_name = player2.nick if player2.nick else player2.name

        self.player1 = player1
        self.player2 = player2

        self.player_obj_dict = {
            player1 : Player(player1_name, "💙"),
            player2 : Player(player2_name, "❤️")
        }

        #Display embed for when players are choosing moves
        self.choices_embed = discord.Embed(colour = discord.Colour.greyple(), description=self.make_health_str())
        self.choices_embed.set_footer(text = f"{player1_name}, {player2_name} please pick your combination")
        self.choices_embed.add_field(name = player1_name, value = "___")
        self.choices_embed.add_field(name = player2_name, value = "___")
        self.choices_embed.set_author(name=f"{player1_name} 🆚 {player2_name}")
        
        self.interaction = interaction

    async def run_game(self) -> None:
        action_view = ActionView(self.player1, self.player2, self.choices_embed, self.player_obj_dict)
        await self.interaction.response.send_message(embed = self.choices_embed, view = action_view)

        #Run the game while both players have health > 0
        #TODO: Add break statement when game finishes
        while True:
            #Wait for user input
            await action_view.wait()

            #Output results by replacing the choices_embed with the new results_embed
            results_embed = discord.Embed(title = "Results:", description=self.make_health_str())
            
            for x in range(3):
                embed_field_value, versus_str = await self.do_compare()
                results_embed.description = self.make_health_str()
                results_embed.add_field(name= f"Round {x} - {versus_str}", value = embed_field_value, inline = False)
                await self.interaction.edit_original_response(embed = results_embed, view = None)
                await asyncio.sleep(7)
            
            await self.interaction.edit_original_response(embed=results_embed)

            
            #Refreshes action view and replace current embed with the choices_embed
            await asyncio.sleep(5)

            self.choices_embed.clear_fields()
            #Clears slected moves from last round
            for player_obj in self.player_obj_dict.values():
                player_obj.new_round()
                self.choices_embed.add_field(name = player_obj.name, value = "___")

            self.choices_embed.description = self.make_health_str()

            action_view = ActionView(self.player1, self.player2, self.choices_embed, self.player_obj_dict)
            await self.interaction.edit_original_response(embed = self.choices_embed, view = action_view)
            #break
    
    async def do_compare(self) -> tuple:
        p1_obj = self.player_obj_dict[self.player1]
        p2_obj = self.player_obj_dict[self.player2]

        p1_move = p1_obj.get_move()
        p2_move = p2_obj.get_move()

        p1_obj.reset_health_diff()
        p2_obj.reset_health_diff()

        versus_str = f"{p1_move} vs {p2_move}"
        if p1_move == p2_move:
            return "Nothing happened...", versus_str
        
        if p1_move.lose_against(p2_move):
            return p2_move.execute(receiver= p1_obj, attacker = p2_obj), versus_str
            
        if p2_move.lose_against(p1_move):
            return p1_move.execute(receiver = p2_obj, attacker = p1_obj), versus_str
    
    def make_health_str(self):
        p1_obj = self.player_obj_dict[self.player1]
        p2_obj = self.player_obj_dict[self.player2]

        player1_str = f"{p1_obj.name}\n{self.make_health_bar(p1_obj)}"
        player2_str = f"{p2_obj.name}\n{self.make_health_bar(p2_obj)}"
        
        return player1_str + "\n\n" + player2_str
            
    def make_health_bar(self, player_boj : Player) -> str:
        health = player_boj.health

        max_health = 100
        max_bars = 20

        dash_convert = int(max_health/max_bars)
        health_display = "=" * int(health/dash_convert)
        missing_health_display = "-" * (max_bars - int(health/dash_convert))

        health_diff_str = f"({player_boj.health_diff})" if player_boj.health_diff else ""
        return "|" + health_display + f"| {health} " + player_boj.emoji + health_diff_str