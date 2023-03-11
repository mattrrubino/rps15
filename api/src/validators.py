def validUsername(username: str) -> bool:
    if len(username) < 1 or len(username) > 32:
        return False

    return True


def validPassword(password: str) -> bool:
    if len(password) < 8 or len(password) > 32:
        return False

    return True
