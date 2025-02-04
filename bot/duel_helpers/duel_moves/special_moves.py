from basic_moves import LightAttack, HeavyAttack, Block
import random

#Chance to double strike with light attack
class Followup(LightAttack):
    def __init__(self) -> None:
        super().__init__()
        self.min_dmg, self.max_dmg = 6, 12
    
    def execute(self, receiver = None, attacker = None):
        super().execute(receiver, attacker)
        
        if random.random() < 0.5:
            return super().execute(receiver, attacker)
    
    def __str__(self) -> str:
        return "👆"