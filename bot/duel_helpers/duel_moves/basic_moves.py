import json
import random

from bot.duel_helpers.duel_moves.move import Move

NOTHINGID = 0
LIGHTID = 1
HEAVYID = 2
BLOCKID = 3

with open("bot/duel_helpers/basic_duel_message.json", 'r') as f:
    MESSAGE_DICT = json.load(f)

LIGHT_MESSAGES = MESSAGE_DICT["light attack"]
HEAVY_MESSAGES = MESSAGE_DICT["heavy attack"]
BLOCK_MESSAGES = MESSAGE_DICT["block"]

NOTHING_URL = "https://i.kym-cdn.com/photos/images/newsfeed/001/057/927/eac.gif"

class DoNothing(Move):
    def __init__(self) -> None:
        super().__init__("NA", NOTHINGID, [])
    
    def lose_against(self, other_move: object) -> bool:
        return other_move.id != BLOCKID
    
    def __str__(self) -> str:
        return "🤷‍♂️"

class LightAttack(Move):
    def __init__(self) -> None:
        super().__init__("Light", LIGHTID, [BLOCKID])
    
    def execute(self, receiver = None, attacker = None):
        damage = random.randint(6, 12)
        receiver.take_damage(damage)
        message, gif_url = random.choice(list(LIGHT_MESSAGES.items()))
        super().execute(receiver, attacker)
        return message.format(attacker.name, receiver.name), gif_url
    
    def __str__(self) -> str:
        return "👆"

class HeavyAttack(Move):
    def __init__(self) -> None:
        super().__init__("Heavy", HEAVYID, [LIGHTID])
    
    def execute(self, receiver = None, attacker = None):
        damage = random.randint(13, 18)
        receiver.take_damage(damage)
        message, gif_url = random.choice(list(HEAVY_MESSAGES.items()))
        super().execute(receiver, attacker)
        return message.format(attacker.name, receiver.name), gif_url

    def __str__(self) -> str:
        return "🥊"

class Block(Move):
    def __init__(self) -> None:
        super().__init__("Block", BLOCKID, [HEAVYID])
    
    def execute(self, receiver = None, attacker = None):
        if receiver.has_next_move():
            receiver.stun()
            message, gif_url = random.choice(list(BLOCK_MESSAGES.items()))
            super().execute(receiver, attacker)
            return message.format(attacker.name, receiver.name), gif_url
            
        return "Nothing happened...(It's the last move)", NOTHING_URL
    
    def __str__(self) -> str:
        return "🛡️"