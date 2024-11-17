import bcrypt


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode(), salt)
    return password_hash.hex()


def validate_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), bytes.fromhex(password_hash))
