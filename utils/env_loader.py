import os
from dotenv import load_dotenv


def load_env():
    """Load var from .env fold and return in a dict"""
    load_dotenv()

    env = {
        "db_name": os.getenv("DB_NAME"),
        "user": os.getenv("USER"),
        "password": os.getenv("PASSWORD"),
        "host": os.getenv("HOST")
    }

    # validation in case of missing vars
    missing = [k for k, v in env.items() if v is None]
    if missing:
        raise RuntimeError(f"Missing env vars: {', '.join(missing)}")

    return env


print(load_env())
