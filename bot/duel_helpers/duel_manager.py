import discord
import asyncio

from bot.util.action_view import ActionView

class DuelManager:
    #Runs the duel match until either side loses(gets to 0 hp)
    def __init__(self, player1 : discord.User, player2: discord.User, interaction) -> None:
        
        self.player1_name = player1.nick if player1.nick else player1.name
        self.player2_name = player2.nick if player2.nick else player2.name

        #Display embed for when players are choosing moves
        self.choices_embed = discord.Embed(colour = discord.Colour.greyple())
        self.choices_embed.set_footer(text = f"{self.player1_name}, {self.player2_name} please pick your combination")
        self.choices_embed.add_field(name = self.player1_name, value = "___", inline = False)
        self.choices_embed.add_field(name = self.player2_name, value = "___", inline = False)
        self.choices_embed.set_author(name=f"{self.player1_name} 🆚 {self.player2_name}")
        
        #Action view object for keeping track of player inputs using discord UI objects
        self.action_view = ActionView(player1, player2, self.choices_embed)
        self.interaction = interaction

        self.health_dict = {player1 : 100, player2 : 100}

    async def run_game(self) -> None:
        await self.interaction.response.send_message(embed = self.choices_embed, view = self.action_view)

        #Run the game while both players have health > 0
        while not 0 in list(self.health_dict.values()):
            #Wait for user input
            await self.action_view.wait()

            #Retrives player inputs and calculate result
            move_dict = self.action_view.get_moves()

            #Output results by replacing the choices_embed with the new results_embed
            results_embed = discord.Embed()
            await self.interaction.response.edit_message(embed=results_embed)

            #Refreshes action view and replace current embed with the choices_embed
            await asyncio.sleep(5)
            self.action_view.new_round()
            await self.interaction.response.edit_message(embed = self.choices_embed, view=self.action_view)


            