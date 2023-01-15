import discord
import asyncio

from bot.util.action_view import ActionView
from bot.duel_helpers.player import Player

NOTHING_URL = "https://i.kym-cdn.com/photos/images/newsfeed/001/057/927/eac.gif"
NOCONTEST_URL = "https://media.tenor.com/MAn0YqfO1isAAAAC/no-contest-super-smash-brothers.gif"
VICTORY_URL = "https://thumbs.gfycat.com/SoggyJoyousCockatiel-size_restricted.gif"
FORFEIT_URL = "https://media.tenor.com/U0D6jtPHPeEAAAAC/paz-white-flag.gif"
IDLE_URL = "https://media.tenor.com/6vEudwCrEAwAAAAd/idle-animation-fighting-games.gif"
MAX_AFK = 2
MAX_ROUNDS = 30

class DuelManager:
    #Runs the duel match until either side loses(gets to 0 hp)
    def __init__(self, player1 : discord.User, player2: discord.User, interaction) -> None:
        player1_name = player1.nick if player1.nick else player1.name
        player2_name = player2.nick if player2.nick else player2.name

        self.player1 = player1
        self.player2 = player2

        self.player1_obj = Player(name = player1_name, emoji = "💙", field_id = 0)
        self.player2_obj = Player(name = player2_name, emoji = "❤️", field_id = 1)

        self.player_obj_dict = {
            player1 : self.player1_obj,
            player2 : self.player2_obj
        }

        #Display embed for when players are choosing moves
        self.choices_embed = discord.Embed(description=self.make_health_str(), color=discord.Colour.red())
        self.choices_embed.set_footer(text = "Pick your combos!")
        self.choices_embed.add_field(name = player1_name, value = "___")
        self.choices_embed.add_field(name = player2_name, value = "___")
        self.choices_embed.set_author(name=f"{player1_name} 🆚 {player2_name}")
        self.choices_embed.set_image(url = IDLE_URL)
        
        self.interaction = interaction

        self.both_afk_count = 0

    async def run_game(self) -> None:
        round_count = 1
        while True:
            if round_count == MAX_ROUNDS:
                await self.end_game(msg = "Bruh 30 rounds is too much. Nope. Bye bye.")
                return

            action_view = ActionView(self.player1, self.player2, self.choices_embed, self.player_obj_dict)
            await self.interaction.edit_original_response(embed = self.choices_embed, view = action_view)
            #Wait for user input
            await action_view.wait()

            if action_view.forfeit_user:
                await self.end_game(forfeit_user=action_view.forfeit_user)
                return
            
            if self.check_afk():
                await self.end_game(msg="Both players afk'd! I'm calling it!")
                return
            #Output results by replacing the choices_embed with the new results_embed
            results_embed = discord.Embed(title = "Results:", description=self.make_health_str(), color=discord.Colour.fuchsia())

            #Loop through all three moves of both users, compare and show winner of each move
            for x in range(3):
                (embed_field_value, gif_url), versus_str = await self.do_compare()

                results_embed.description = self.make_health_str()
                results_embed.add_field(name= f"Move {x+1} - {versus_str}", value = embed_field_value, inline = False)
                results_embed.set_image(url = gif_url)
                
                await self.interaction.edit_original_response(embed = results_embed, view = None)
                await asyncio.sleep(6)
                
                if self.is_finished():
                    await self.end_game()
                    return

            #Refreshes action view and replace current embed with the choices_embed
            self.choices_embed.clear_fields()
            #Clears slected moves from last round
            for player_obj in self.player_obj_dict.values():
                player_obj.new_round()
                self.choices_embed.add_field(name = player_obj.name, value = "___")

            self.choices_embed.description = self.make_health_str()
            round_count += 1
    
    async def do_compare(self):
        p1_move = self.player1_obj.get_move()
        p2_move = self.player2_obj.get_move()

        self.player1_obj.reset_health_diff()
        self.player2_obj.reset_health_diff()

        versus_str = f"{p1_move} vs {p2_move}"
        if p1_move == p2_move:
            return ("Nothing happened...", NOTHING_URL), versus_str
        
        if p1_move.lose_against(p2_move):
            return p2_move.execute(receiver= self.player1_obj, attacker = self.player2_obj), versus_str
            
        if p2_move.lose_against(p1_move):
            return p1_move.execute(receiver = self.player2_obj, attacker = self.player1_obj), versus_str
    
    def make_health_str(self):
        player1_str = f"{self.player1_obj.name}\n{self.make_health_bar(self.player1_obj)}"
        player2_str = f"{self.player2_obj.name}\n{self.make_health_bar(self.player2_obj)}"
        
        return player1_str + "\n" + player2_str
            
    def make_health_bar(self, player_boj : Player) -> str:
        health = player_boj.health

        max_health = 100
        max_bars = 20

        dash_convert = int(max_health/max_bars)
        health_display = "=" * int(health/dash_convert)
        missing_health_display = "-" * (max_bars - int(health/dash_convert))

        health_diff_str = f"({player_boj.health_diff})" if player_boj.health_diff else ""
        return "|" + health_display + f"| {health} " + player_boj.emoji  + health_diff_str
    
    def is_finished(self):
        return self.player1_obj.health <= 0 or self.player2_obj.health <= 0

    #just ike the marvel movie
    async def end_game(self, msg = "Match Results🏆", forfeit_user = None):
        embed = discord.Embed(title = msg, color=discord.Colour.green())

        p1_health = self.player1_obj.health
        p2_health = self.player2_obj.health
        
        p1_name = self.player1_obj.name
        p2_name = self.player2_obj.name

        if p1_health <= 0 and p2_health <= 0:
            embed.description = "Double KO! It's a draw!"
            embed.set_image(url = NOCONTEST_URL)
        elif p1_health <= 0:
            embed.description = f"**{p2_name}** wins!"
            embed.set_image(url = VICTORY_URL)
            embed.set_thumbnail(url = self.player2.avatar)
        elif p2_health <= 0:
            embed.description = f"**{p1_name}** wins!"
            embed.set_image(url = VICTORY_URL)
            embed.set_thumbnail(url = self.player1.avatar)
        elif forfeit_user:
            embed.description = f"{forfeit_user.mention} has forfeited...lol"
            embed.set_footer(text = "Guess someone was too scared...")
            embed.set_image(url = FORFEIT_URL)
            embed.color = discord.Colour.dark_blue()
            embed.set_thumbnail(url = forfeit_user.avatar)
        else:
            embed.description = "No one wins!"
            embed.set_image(url = NOCONTEST_URL)
        
        await self.interaction.edit_original_response(embed = embed, view = None)

    def check_afk(self):
        if not self.player1_obj.moves and not self.player2_obj.moves:
            self.both_afk_count += 1
        else:
            self.both_afk_count = 0
        
        if self.both_afk_count == MAX_AFK:
            return True
        else:
            return False