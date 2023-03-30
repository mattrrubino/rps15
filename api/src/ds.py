import asyncio
import threading
from src.rps import Player, Game


class Matcher:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.queue = None

    # TODO: What if close sent during queue put?
    async def match(self, playerA: Player):
        game = None

        with self.lock:
            playerB = self.queue

            if playerB:
                # Create the game and notify other player's thread
                game = Game(playerA, playerB)
                await playerB.game.put(game)
                self.queue = None

                # Start the game thread
                asyncio.create_task(game.run())
            else:
                self.queue = playerA

        if game is None:
            gameTask = asyncio.create_task(playerA.game.get())
            messageTask = asyncio.create_task(playerA.connection.receive())

            # Try to read game from other player's thread
            while game is None:
                done, _ = await asyncio.wait(
                    [gameTask, messageTask],
                    return_when=asyncio.FIRST_COMPLETED
                )

                for task in done:
                    if task is gameTask:
                        game = task.result()
                    else:
                        message = task.result()

                        # Clear Matcher if client disconnects in queue
                        if message["type"] == "websocket.disconnect":
                            gameTask.cancel()
                            with self.lock:
                                self.queue = None
                            return

                        messageTask = asyncio.create_task(playerA.connection.receive())

        try:
            await game.runPlayer(playerA)
        except asyncio.CancelledError:
            pass
