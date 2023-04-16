import secrets
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from data import MOVES
from cli import DEV


hostname = "localhost" if DEV else "mongo"
client = AsyncIOMotorClient(hostname)
rps = client["RPS"]

user = rps["User"]
session = rps["Session"]


#region User Data

async def getUser(username: str) -> Optional[dict]:
    userData = await user.find_one({"Username": username})
    if userData:
        del userData["_id"]

    return userData


async def createUser(username: str, password: str) -> dict:
    userData = {
        "Username": username,
        "Password": password,
        "Wins": 0,
        "Losses": 0,
        "Elo": 1000,
        "MoveCounts": {move: 0 for move in MOVES}
    }

    return await user.insert_one(userData)


async def incrementUserWins(username: str) -> None:
    await user.update_one(
        {"Username": username},
        { "$inc": { "Wins": 1 } },
    )


async def incrementUserLosses(username: str) -> None:
    await user.update_one(
        {"Username": username},
        { "$inc": { "Losses": 1 } },
    )


async def incrementUserMove(username: str, move: str) -> None:
    await user.update_one(
        {"Username": username},
        { "$inc": { f"MoveCounts.{move}": 1 } },
    )

#endregion


#region Session Data

async def getSessionUsername(token: str) -> Optional[str]:
    sessionData = await session.find_one({"Token": token})
    if sessionData:
        return sessionData["Username"]
    return sessionData


async def deleteSession(token: str) -> None:
    await session.delete_many({"Token": token})


async def createSession(username: str) -> str:
    await deleteSession(username)

    token = secrets.token_urlsafe(32)
    await session.insert_one({"Username": username, "Token": token})

    return token

#endregion
