import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password=password.encode("utf-8"),
        salt=bcrypt.gensalt()
    ).decode("utf-8")


def check_password(passowrd: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password=passowrd.encode("utf-8"),
        hashed_password=hashed_password.encode("utf-8")
    )
