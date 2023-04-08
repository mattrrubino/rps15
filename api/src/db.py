import secrets
from typing import Optional
from pymongo import MongoClient
from data import MOVES


# TODO: Change to "mongo"
client = MongoClient("localhost")
rps = client["RPS"]

user = rps["User"]
session = rps["Session"]


#region User Data

def getUser(username: str) -> Optional[dict]:
    userData = user.find_one({"Username": username})
    if userData:
        del userData["_id"]

    return userData


def createUser(username: str, password: str) -> dict:
    userData = {
        "Username": username,
        "Password": password,
        "Wins": 0,
        "Losses": 0,
        "Elo": 1000,
        "MoveCounts": {move: 0 for move in MOVES}
    }

    return user.insert_one(userData)


def incrementUserWins(username: str) -> None:
    user.update_one(
        {"Username": username},
        { "$inc": { "Wins": 1 } },
    )


def incrementUserLosses(username: str) -> None:
    user.update_one(
        {"Username": username},
        { "$inc": { "Losses": 1 } },
    )


def incrementUserMove(username: str, move: str) -> None:
    user.update_one(
        {"Username": username},
        { "$inc": { f"MoveCounts.{move}": 1 } },
    )

#endregion


#region Session Data

def getSessionUsername(token: str) -> Optional[str]:
    sessionData = session.find_one({"Token": token})
    if sessionData:
        return sessionData["Username"]
    return sessionData


def deleteSession(token: str) -> None:
    session.delete_many({"Token": token})


def createSession(username: str) -> str:
    deleteSession(username)

    token = secrets.token_urlsafe(32)
    session.insert_one({"Username": username, "Token": token})

    return token

#endregion
