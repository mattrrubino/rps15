// WebSocket connection for one game
let game;

function OpenGame() {
    if (game)
        CloseGame()

    const protocol = window.location.protocol === "https:" ? "wss://" : "ws://"
    game = new WebSocket(protocol + window.location.host + "/api/game")
    game.onerror = () => alert("You must create an account and log in before you can play.")
    game.onopen = () => {
        setTimeout(() => { if (window.location.toString().search("/game") === -1) alert("You have entered the queue. Waiting for another player.") }, 1000)
    }
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
