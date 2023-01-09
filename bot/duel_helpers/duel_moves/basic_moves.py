import discord
import random

from bot.duel_helpers.duel_moves.move import Move

NOTHINGID = 0
LIGHTID = 1
HEAVYID = 2
BLOCKID = 3

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
        damage = random.randint(3, 7)
        receiver.take_damage(damage)
        
        return f"{attacker} dealt {damage} damage to {receiver}!"
    
    def __str__(self) -> str:
        return "👆"

class HeavyAttack(Move):
    def __init__(self) -> None:
        super().__init__("Heavy", HEAVYID, [LIGHTID])
    
    def execute(self, receiver = None, attacker = None):
        damage = random.randint(10, 15)
        receiver.take_damage(damage)
        return f"{attacker} dealt {damage} damage to {receiver}!"

    def __str__(self) -> str:
        return "🥊"

class Block(Move):
    def __init__(self) -> None:
        super().__init__("Block", BLOCKID, [HEAVYID])
    
    def execute(self, receiver = None, attacker = None):
        if receiver.has_next_move():
            receiver.stun()
            return f"{attacker} blocked an attack from {receiver}! {receiver} is stunned!"
        return "Nothing happened..."
    
    def __str__(self) -> str:
        return "🛡️"