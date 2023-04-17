import json
import html
import asyncio
import random
from data import MOVES, VERBS
from db import incrementUserWins, incrementUserLosses, incrementUserMove, transferUserElo


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

    def toMessage(self, playerA: bool) -> dict:
        obj = {
            "operation": "end_round",
            "move": self.playerAMove if playerA else self.playerBMove,
            "opponent_move": self.playerBMove if playerA else self.playerAMove,
            "message": self.message,
        }
        if self.winner:
            obj["winner"] = self.winner.username
            obj["loser"] = self.loser.username
        
        return obj


class Round:
    def __init__(self, number: int) -> None:
        self.number = number
        self.moves = {}
        self.done = asyncio.Queue(maxsize=-1)

    async def setPlayerMove(self, player: Player, move: int) -> None:
        if player not in self.moves and move >= 0 and move < len(MOVES):
            self.moves[player] = move

            # Mark round as done
            if len(self.moves) > 1:
                await self.done.put(True)

    def getWinnerLoser(self) -> tuple:
        (p0, mp0), (p1, mp1) = self.moves.items()

        if mp0 == mp1:
            return None, None

        if mp0 < mp1:
            return (p0,p1) if (mp1-mp0 <= 7) else (p1,p0)
        else:
            return (p1,p0) if (mp0-mp1 <= 7) else (p0,p1)

    def getOutcomeMessage(self, winningMoveIndex: int, losingMoveIndex: int) -> str:
        if winningMoveIndex is None and losingMoveIndex is None:
            return "IT'S A TIE"

        winningMove = MOVES[winningMoveIndex]
        losingMove = MOVES[losingMoveIndex]

        verb = VERBS[winningMove].get(losingMove)
        if not verb:
            verb = VERBS[winningMove].get("default")

        return f"{winningMove} {verb} {losingMove}".upper()

    async def getOutcome(self, playerA: Player, playerB: Player) -> RoundOutcome:
        # Sets moves to random if they are not initialized
        await self.setPlayerMove(playerA, random.randint(0, len(MOVES)-1))
        await self.setPlayerMove(playerB, random.randint(0, len(MOVES)-1))

        winner, loser = self.getWinnerLoser()
        message = self.getOutcomeMessage(self.moves[winner] if winner else None, self.moves[loser] if loser else None)

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
        msgA = json.dumps({"operation": "start_game"})
        msgB = json.dumps({"operation": "start_game"})

        await self.playerA.connection.send_text(msgA)
        await self.playerB.connection.send_text(msgB)

    async def endSequence(self, winner: Player, loser: Player) -> None:
        msg = json.dumps({"operation": "end_game", "winner": winner.username, "loser": loser.username})

        await asyncio.gather(
            incrementUserWins(winner.username),
            incrementUserLosses(loser.username),
            transferUserElo(loser.username, winner.username, max(winner.wins - loser.wins, 0)),
        )

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

        # Waits for the round to finish (both players lock a move)
        # Forces round finish after "timeout" seconds
        doneTask = asyncio.create_task(self.round.done.get())
        await asyncio.wait([doneTask], timeout=16)

        outcome = await self.round.getOutcome(self.playerA, self.playerB)

        await incrementUserMove(self.playerA.username, MOVES[outcome.playerAMove])
        await incrementUserMove(self.playerB.username, MOVES[outcome.playerBMove])

        if outcome.winner:
            outcome.winner.wins += 1

        msgA = outcome.toMessage(True)
        msgA["you"] = self.playerA.wins
        msgA["opponent"] = self.playerB.wins
        msgA = json.dumps(msgA)

        msgB = outcome.toMessage(False)
        msgB["you"] = self.playerB.wins
        msgB["opponent"] = self.playerA.wins
        msgB = json.dumps(msgB)

        await self.playerA.connection.send_text(msgA)
        await self.playerB.connection.send_text(msgB)

    async def handleGame(self):
        await self.startSequence()

        while not self.isDone():
            await asyncio.sleep(5)
            self.nextRound()
            await self.roundSequence()

        await asyncio.sleep(5)
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
            elif operation == "get_names":
                response = json.dumps({"operation": "send_names", "you": player.username, "opponent": opponent.username})
                await player.connection.send_text(response)
            elif operation == "send_move":
                # Ignore move if index is not supplied or is invalid
                move = obj.get("move")
                if move is None or move < 0 or move >= len(MOVES):
                    continue

                await self.round.setPlayerMove(player, move)
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
