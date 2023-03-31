import asyncio
import threading
from src.rps import Player, Game


class Matcher:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.queue = None, None

    async def match(self, playerA: Player):
        game = None

        with self.lock:
            playerB, gameChannel = self.queue

            if playerB and gameChannel:
                # Create the game and notify other player's thread
                game = Game(playerA, playerB)
                await gameChannel.put(game)

                self.queue = None, None

                # Run the game thread
                game.runGame()
            else:
                gameChannel = asyncio.Queue()
                self.queue = playerA, gameChannel

        if game is None:
            gameTask = asyncio.create_task(gameChannel.get())
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

                        try:
                            messageTask.cancel()
                        except asyncio.CancelledError:
                            pass

                        break
                    else:
                        message = task.result()

                        # Clear Matcher if client disconnects in queue
                        if message["type"] == "websocket.disconnect":
                            try:
                                gameTask.cancel()
                            except asyncio.CancelledError:
                                pass

                            with self.lock:
                                self.queue = None, None
                            return

                        messageTask = asyncio.create_task(playerA.connection.receive())

        try:
            await game.runPlayer(playerA)
        except asyncio.CancelledError:
            pass
