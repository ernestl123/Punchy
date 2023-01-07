import discord
import random

from move import Move

NOTHINGID = 0
LIGHTID = 1
HEAVYID = 2
BLOCKID = 3

class DoNothing(Move):
    def __init__(self) -> None:
        super().__init__("NA", NOTHINGID, [])
    
    def lose_against(self, _: object) -> bool:
        return True
        
class LightAttack(Move):
    def __init__(self) -> None:
        super().__init__("Light", LIGHTID, [BLOCKID])
    
    def execute(self, player_info_dict=None, receiver: discord.User = None, **_):
        player_info_dict[receiver]["health"] -= max(0, player_info_dict[receiver]["health"] - random.randint(3, 7))
        
class HeavyAttack(Move):
    def __init__(self) -> None:
        super().__init__("Heavy", HEAVYID, [LIGHTID])
    
    def execute(self, player_info_dict=None, receiver = None, **_):
        player_info_dict[receiver]["health"] -= max(0, player_info_dict[receiver]["health"] - random.randint(10, 15))

class Block(Move):
    def __init__(self) -> None:
        super().__init__("Block", BLOCKID, [HEAVYID])
    
    def execute(self, player_info_dict = None, receiver = None, **_):
        player_info_dict[receiver]["moves"][1] = DoNothing()
        return
    