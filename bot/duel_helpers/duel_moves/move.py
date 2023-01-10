class Move:
    def __init__(self, name: str, id: id, lose_list: list) -> None:
        self.name = name
        self.id = id
        self.lose_list = lose_list
    
    def lose_against(self, other_move: object) -> bool:
        if not other_move:
            return False

        return other_move.id in self.lose_list
    
    def execute(self, receiver = None, attacker = None):
        return
    
    def __eq__(self, __o: object) -> bool:
        return __o.id == self.id