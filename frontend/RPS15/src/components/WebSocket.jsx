// WebSocket connection for one game
let game;

function OpenGame() {
    if (game)
        CloseGame()

    // TODO: Might need to change this to /api/game in production
    // For some reason, Vite WebSocket proxies do not work :(
    // (I intentionally removed it from the config b/c it was not working)
    game = new WebSocket("ws://localhost:8000/game")
}

function SetOnMessage(handler) {
    if (game)
        game.onmessage = handler
}

function SetOnClose(handler) {
    if (game)
        game.onclose = handler
}

function CloseGame() {
    if (game) {
        game.close()
        game = undefined
    }
}

function Send(text) {
    if (game)
        game.send(text)
}

export {
    OpenGame,
    CloseGame,
    SetOnMessage,
    SetOnClose,
    Send,
}
