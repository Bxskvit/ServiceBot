import os
from dotenv import load_dotenv  # getting bot token from dotenv


def get_telegram_token() -> str:
    load_dotenv(dotenv_path="config\\.env")
    token = os.getenv('TELEGRAM_TOKEN')
    return token


def get_db_path() -> str:
    load_dotenv(dotenv_path="config\\.env")
    token = os.getenv('DATABASE')
    return token
