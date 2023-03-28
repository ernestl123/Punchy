from bot.duel_helpers.duel_moves.basic_moves import *

DEFAULT_MOVES = [LightAttack(), HeavyAttack(), Block()]

class Player:
    def __init__(self, name, emoji, field_id, move_options = DEFAULT_MOVES) -> None:
        self.name = f"**{name}**"
        self.moves = list()
        self.move_options = move_options
        self.field_id = field_id
        self.emoji = emoji
        self.health = 1
        self.health_diff = 0
        self.last_hit = ""

    def take_damage(self, damage : int):
        self.health = max(0,  self.health - damage)
        self.health_diff -= damage
    
    def heal(self, heal_amount : int):
        self.health = max(100,  self.health + heal_amount)
        self.health_diff += heal_amount

    def add_light(self):
        self.moves.append(self.move_options[0])
    
    def add_heavy(self):
        self.moves.append(self.move_options[1])
    
    def add_block(self):
        self.moves.append(self.move_options[2])
    
    def reset_health_diff(self):
        self.health_diff = 0
        
    def new_round(self):
        self.last_hit = ""
        self.moves = list()
        self.health_diff = 0

    def stun(self):
        self.moves[0] = DoNothing()
    
    def get_move(self):
        if not self.moves:
            return DoNothing()

        return self.moves.pop(0)

    def has_next_move(self):
        return len(self.moves) >= 1
    
    def __str__(self) -> str:
        return self.name