import json
import html
import asyncio
import random
from src.data import MOVES, VERBS
from src.db import incrementUserWins, incrementUserLosses, incrementUserMove


class Player:
    def __init__(self, username: str, connection):
        self.username = username
        self.connection = connection
        self.wins = 0


class RoundOutcome:
    def __init__(self, playerAMove: int, playerBMove: int, message: str, winner: Player, loser: Player) -> None:
        self.playerAMove = playerAMove
        self.playerBMove = playerBMove
        self.message = message
        self.winner = winner
        self.loser = loser

    def toMessage(self, playerA: bool) -> str:
        obj = {
            "operation": "end_round",
            "move": self.playerAMove if playerA else self.playerBMove,
            "opponent_move": self.playerBMove if playerA else self.playerAMove,
            "message": self.message,
        }
        if self.winner:
            obj["winner"] = self.winner.username
            obj["loser"] = self.loser.username
        
        return json.dumps(obj)


class Round:
    def __init__(self, number: int) -> None:
        self.number = number
        self.moves = {}

    def setPlayerMove(self, player: Player, move: int) -> None:
        if player not in self.moves and move >= 0 and move < len(MOVES):
            self.moves[player] = move

    def getWinnerLoser(self) -> tuple:
        (p0, mp0), (p1, mp1) = self.moves.items()

        if mp0 == mp1:
            return None

        if mp0 < mp1:
            return (p0,p1) if (mp1-mp0 <= 7) else (p1,p0)
        else:
            return (p1,p0) if (mp0-mp1 <= 7) else (p0,p1)

    def getOutcomeMessage(self, winningMoveIndex: int, losingMoveIndex: int) -> str:
        winningMove = MOVES[winningMoveIndex]
        losingMove = MOVES[losingMoveIndex]

        verb = VERBS[winningMove].get(losingMove)
        if not verb:
            verb = VERBS[winningMove].get("default")

        message = f"{winningMove} {verb} {losingMove}".upper()

        return message

    def getOutcome(self, playerA: Player, playerB: Player) -> RoundOutcome:
        # Sets moves to random if they are not initialized
        self.setPlayerMove(playerA, random.randint(0, len(MOVES)-1))
        self.setPlayerMove(playerB, random.randint(0, len(MOVES)-1))

        winner, loser = self.getWinnerLoser()
        message = self.getOutcomeMessage(self.moves[winner], self.moves[loser])

        return RoundOutcome(self.moves[playerA], self.moves[playerB], message, winner, loser)


class Game:
    def __init__(self, playerA: Player, playerB: Player):
        self.playerA = playerA
        self.playerB = playerB
        self.round = Round(0)
        self.handlerTasks = []

    def isDone(self) -> bool:
        return self.playerA.wins >= 3 or self.playerB.wins >= 3

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

    async def endSequence(self, winner: Player, loser: Player) -> None:
        msg = json.dumps({"operation": "end_game", "winner": winner.username, "loser": loser.username})

        incrementUserWins(winner.username)
        incrementUserLosses(loser.username)

        # Try sending on A's connection
        try:
            await self.playerA.connection.send_text(msg)
        except RuntimeError:
            pass

        # Try sending on B's connection
        try:
            await self.playerB.connection.send_text(msg)
        except RuntimeError:
            pass

        self.kill()

    async def roundSequence(self):
        msg = json.dumps({"operation": "start_round", "number": self.getRoundNumber()})

        await self.playerA.connection.send_text(msg)
        await self.playerB.connection.send_text(msg)

        # TODO: Exit early if both players have selected
        await asyncio.sleep(5)

        outcome = self.round.getOutcome(self.playerA, self.playerB)

        incrementUserMove(self.playerA.username, MOVES[outcome.playerAMove])
        incrementUserMove(self.playerB.username, MOVES[outcome.playerBMove])

        await self.playerA.connection.send_text(outcome.toMessage(True))
        await self.playerB.connection.send_text(outcome.toMessage(False))

        if outcome.winner:
            outcome.winner.wins += 1

    async def handleGame(self):
        await self.startSequence()

        while not self.isDone():
            self.nextRound()
            await self.roundSequence()

        if self.playerA.wins > self.playerB.wins:
            await self.endSequence(self.playerA, self.playerB)
        else:
            await self.endSequence(self.playerB, self.playerA)

    async def handlePlayer(self, player: Player, opponent: Player):
        while True:
            msg = await player.connection.receive()

            # Ignore message without WebSocket message type
            t = msg.get("type")
            if t is None:
                continue

            # Surrender the game if the client closes the connection
            if t == "websocket.disconnect":
                await self.endSequence(opponent, player)
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

                response = json.dumps({"operation": "send_message", "username": player.username, "message": html.escape(message)})
                await player.connection.send_text(response)
                await opponent.connection.send_text(response)
            elif operation == "send_move":
                # Ignore move if index is not supplied or is invalid
                move = obj.get("move")
                if move is None or move < 0 or move >= len(MOVES):
                    continue

                self.round.setPlayerMove(player, move)
            else:
                # Unknown operation sent
                pass

    def runGame(self):
        task = asyncio.create_task(self.handleGame())
        self.handlerTasks.append(task)
        return task

    def runPlayer(self, player: Player):
        if player is self.playerA:
            opponent = self.playerB
        else:
            opponent = self.playerA

        task = asyncio.create_task(self.handlePlayer(player, opponent))
        self.handlerTasks.append(task)
        return task
