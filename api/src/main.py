import bcrypt
from fastapi import FastAPI, Response, WebSocket, Form, Cookie
from src.validators import validUsername, validPassword
from src.db import getUser, createUser, getSessionUsername, createSession, deleteSession


app = FastAPI()


#region User Authentication

@app.post("/register", status_code=201)
async def register(response: Response, username: str = Form(), password: str = Form(), confirmPassword: str = Form()):
    # Cannot register with invalid form fields
    if not validUsername(username) or not validPassword(password) or password != confirmPassword:
        response.status_code = 400
        return "Bad Request"

    # Cannot register a username that already exists
    if getUser(username) is not None:
        response.status_code = 409
        return "Conflict"

    # Create user data
    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(password.encode(), salt)
    createUser(username, hashedPassword)

    # Create session data
    token = createSession(username)
    response.set_cookie("token", token, httponly=True)


@app.post("/login")
async def login(response: Response, username: str = Form(), password: str = Form()):
    # Cannot log in with invalid form fields
    if not validUsername(username) or not validPassword(password):
        response.status_code = 400
        return "Bad Request"

    # Cannot log in with username that does not exist
    user = getUser(username)
    if not user:
        response.status_code = 404
        return "Not Found"

    # Cannot log in with incorrect password
    hashedPassword = user["Password"]
    if not bcrypt.checkpw(password.encode(), hashedPassword):
        response.status_code = 403
        return "Forbidden"

    # Create session data
    token = createSession(username)
    response.set_cookie("token", token, httponly=True)


@app.post("/logout")
async def logout(response: Response, token: str = Cookie()):
    # Revoke session data
    deleteSession(token)
    response.delete_cookie("token", httponly=True)

    # Redirect to login page
    response.status_code = 301
    response.headers["Location"] = "/login"

#endregion


#region User Data

@app.get("/user/{username}")
async def user(response: Response, username: str) -> dict:
    # Cannot look up invalid username
    if not validUsername(username):
        response.status_code = 400
        return "Bad Request"

    # Cannot look up user that does not exist
    user = getUser(username)
    if not user:
        response.status_code = 404
        return "Not Found"

    # Do not expose user's password hash publicly
    del user["Password"]

    return user

#endregion


#region Matchmaking

@app.websocket("/matchmaking")
async def matchmaking(ws: WebSocket, response: Response, token: str = Cookie()):
    # Cannot connect to matchmaking with invalid session token
    username = getSessionUsername(token)
    if username is None:
        await ws.close()
        response.status_code = 403
        return "Forbidden"

    await ws.accept()

    # TODO: Matchmaking code here
    await ws.send_text("Connected to matchmaking!")
    await ws.close()

#endregion


#region Game

@app.websocket("/game/{gameId}")
async def game(ws: WebSocket, response: Response, gameId: str, token: str = Cookie()):
    # Cannot connect to game with invalid session token
    username = getSessionUsername(token)
    if username is None:
        await ws.close()
        response.status_code = 403
        return "Forbidden"

    # TODO: Check if this user belongs to this game

    await ws.accept()

    # TODO: Game code here
    await ws.send_text(f"Connected to game {gameId}!")
    await ws.close()

#endregion
