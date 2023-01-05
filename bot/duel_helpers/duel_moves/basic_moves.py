from move import Move

LIGHTID = 1
HEAVYID = 2
BLOCKID = 3

class LightAttack(Move):
    def __init__(self) -> None:
        super().__init__("Light", LIGHTID, [BLOCKID])

class HeavyAttack(Move):
    def __init__(self) -> None:
        super().__init__("Heavy", HEAVYID, [LIGHTID])

class Block(Move):
    def __init__(self) -> None:
        super().__init__("Block", BLOCKID, [HEAVYID])
    