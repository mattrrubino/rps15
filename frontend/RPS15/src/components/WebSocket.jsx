// WebSocket connection for one game
let game;

function OpenGame() {
    if (game)
        CloseGame()

    const protocol = window.location.protocol === "https:" ? "wss://" : "ws://"
    game = new WebSocket(protocol + window.location.hostname + "/api/game")
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
