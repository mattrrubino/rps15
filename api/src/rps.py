import json
from asyncio import Queue


MOVES = [
    "rock", "fire", "scissors", "snake", "human",
    "tree", "wolf", "sponge", "paper", "air", "water",
    "dragon", "devil", "lightning", "gun",
]


class Player:
    def __init__(self, username: str, connection):
        self.username = username
        self.connection = connection
        self.game = Queue()


class Game:
    def __init__(self, playerA, playerB):
        self.playerA = playerA
        self.playerB = playerB

    async def handlePlayer(self, player: Player):
        if player is self.playerA:
            opponent = self.playerB
        else:
            opponent = self.playerA

        msg = json.dumps({"operation": "start_game", "opponent": opponent.username})
        await player.connection.send_text(msg)

        # TODO: Handle player messages here
