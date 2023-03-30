import json
import asyncio


MOVES = [
    "rock", "fire", "scissors", "snake", "human",
    "tree", "wolf", "sponge", "paper", "air", "water",
    "dragon", "devil", "lightning", "gun",
]


class Player:
    def __init__(self, username: str, connection):
        self.username = username
        self.connection = connection
        self.game = asyncio.Queue()


class Round:
    def __init__(self, number) -> None:
        self.number = number


class Game:
    def __init__(self, playerA, playerB):
        self.playerA = playerA
        self.playerB = playerB
        self.round = Round(1)
        self.handlerTasks = {}

    def isDone(self) -> bool:
        return self.getRound() > 5

    def getRound(self) -> int:
        return self.round.number

    def nextRound(self) -> None:
        self.round = Round(self.round.number+1)

    def kill(self) -> None:
        for handler in self.handlerTasks.values():
            handler.cancel()

    async def run(self):
        msgA = json.dumps({"operation": "start_game", "opponent": self.playerB.username})
        msgB = json.dumps({"operation": "start_game", "opponent": self.playerA.username})

        await self.playerA.connection.send_text(msgA)
        await self.playerB.connection.send_text(msgB)

        await asyncio.sleep(5)

        while not self.isDone():
            msg = json.dumps({"operation": "start_round", "number": self.getRound()})

            await self.playerA.connection.send_text(msg)
            await self.playerB.connection.send_text(msg)

            await asyncio.sleep(5)
            self.nextRound()

        self.kill()

    async def handlePlayer(self, player: Player, opponent: Player):
        await asyncio.sleep(1000)

    def runPlayer(self, player: Player):
        if player is self.playerA:
            opponent = self.playerB
        else:
            opponent = self.playerA

        task = asyncio.create_task(self.handlePlayer(player, opponent))
        self.handlerTasks[player] = task
        return task
