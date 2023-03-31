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


class Round:
    def __init__(self, number) -> None:
        self.number = number


class Game:
    def __init__(self, playerA, playerB):
        self.playerA = playerA
        self.playerB = playerB
        self.round = Round(1)
        self.handlerTasks = []

    def isDone(self) -> bool:
        return self.getRoundNumber() > 5

    def getRoundNumber(self) -> int:
        return self.round.number

    def nextRound(self) -> None:
        self.round = Round(self.round.number+1)

    def kill(self) -> None:
        for handler in self.handlerTasks:
            try:
                handler.cancel()
            except asyncio.CancelledError:
                pass

    async def startSequence(self):
        msgA = json.dumps({"operation": "start_game", "opponent": self.playerB.username})
        msgB = json.dumps({"operation": "start_game", "opponent": self.playerA.username})

        await self.playerA.connection.send_text(msgA)
        await self.playerB.connection.send_text(msgB)

        await asyncio.sleep(5)

    async def roundSequence(self):
        msg = json.dumps({"operation": "start_round", "number": self.getRoundNumber()})

        await self.playerA.connection.send_text(msg)
        await self.playerB.connection.send_text(msg)

        await asyncio.sleep(5)
        self.nextRound()

    async def run(self):
        await self.startSequence()

        while not self.isDone():
            await self.roundSequence()

        self.kill()

    async def handlePlayer(self, player: Player, opponent: Player):
        while True:
            msg = await player.connection.receive()

            # Ignore message without WebSocket message type
            t = msg.get("type")
            if t is None:
                continue

            # Surrender the game if the client closes the connection
            if t == "websocket.close":
                # TODO: Give win to opponent
                self.kill()
                return

            # Ignore message without text
            text = msg.get("text")
            if text is None:
                continue

            # Try to parse message into JSON object
            try:
                obj = json.loads(text)
            except (json.JSONDecodeError, TypeError):
                continue

            # Ignore message without an operation
            operation = obj.get("operation")
            if operation is None:
                continue

            if operation == "send_message":
                # Ignore chat if no message is supplied
                message = obj.get("message")
                if message is None:
                    continue

                response = json.dumps({"operation": "send_message", "username": player.username, "message": message})
                await player.connection.send_text(response)
                await opponent.connection.send_text(response)

    def runPlayer(self, player: Player):
        if player is self.playerA:
            opponent = self.playerB
        else:
            opponent = self.playerA

        task = asyncio.create_task(self.handlePlayer(player, opponent))
        self.handlerTasks.append(task)
        return task
