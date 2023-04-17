import uvicorn
import html
from bcrypt import checkpw
from fastapi import FastAPI, Response, WebSocket, Form, Cookie
from validators import validUsername, validPassword
from db import getUser, createUser, getSessionUsername, createSession, deleteSession
from ds import Matcher
from rps import Player
from cli import DEV


app = FastAPI()


#region User Authentication

@app.post("/register", status_code=201)
async def register(response: Response, username: str = Form(), password: str = Form()):
    # Cannot register with invalid form fields
    if not validUsername(username) or not validPassword(password):
        response.status_code = 400
        return "Bad Request"

    # Prevent HTML injection
    username = html.escape(username)

    # Cannot register a username that already exists
    user = await getUser(username)
    if user is not None:
        response.status_code = 409
        return "Conflict"

    # Create user data
    await createUser(username, password)

    # Create session data
    token = await createSession(username)
    response.set_cookie("token", token, httponly=True, expires=2**30)


@app.post("/login")
async def login(response: Response, username: str = Form(), password: str = Form()):
    # Cannot log in with invalid form fields
    if not validUsername(username) or not validPassword(password):
        response.status_code = 400
        return "Bad Request"

    # Cannot log in with username that does not exist
    user = await getUser(username)
    if not user:
        response.status_code = 404
        return "Not Found"

    # Cannot log in with incorrect password
    hashedPassword = user["Password"]
    if not checkpw(password.encode(), hashedPassword):
        response.status_code = 403
        return "Forbidden"

    # Create session data
    token = await createSession(username)
    response.set_cookie("token", token, httponly=True, expires=2**30)


@app.post("/logout")
async def logout(response: Response, token: str = Cookie()):
    # Revoke session data
    await deleteSession(token)
    response.delete_cookie("token", httponly=True)

#endregion


#region User Data

@app.get("/user/{username}")
async def user(response: Response, username: str) -> dict:
    # Cannot look up invalid username
    if not validUsername(username):
        response.status_code = 400
        return "Bad Request"

    # Cannot look up user that does not exist
    user = await getUser(username)
    if not user:
        response.status_code = 404
        return "Not Found"

    # Do not expose user's password hash publicly
    del user["Password"]

    return user

@app.get("/user")
async def user(response: Response, token: str = Cookie()) -> dict:
    # Cannot get user information with invalid session token
    username = await getSessionUsername(token)
    if username is None:
        response.status_code = 401
        return "Unauthorized"

    # Cannot look up invalid username
    if not validUsername(username):
        response.status_code = 400
        return "Bad Request"

    # Cannot look up user that does not exist
    user = await getUser(username)
    if not user:
        response.status_code = 404
        return "Not Found"

    # Do not expose user's password hash publicly
    del user["Password"]

    return user

#endregion


#region Matchmaking

matcher = Matcher()

@app.websocket("/game")
async def matchmaking(ws: WebSocket, response: Response, token: str = Cookie()):
    # Cannot connect to matchmaking with invalid session token
    username = await getSessionUsername(token)
    if username is None:
        await ws.close()
        response.status_code = 403
        return "Forbidden"

    await ws.accept()

    # Match the player
    player = Player(username, ws)
    await matcher.match(player)

#endregion


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=DEV, proxy_headers=True)
