import bcrypt

"""Хэширует пароль с использованием bcrypt."""


def hash_password(password: str):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password.decode("utf-8")
