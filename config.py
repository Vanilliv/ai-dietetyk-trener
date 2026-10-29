# Wczytywanie pliku .env i ustawienia połączenia
import os
import sys
from dotenv import load_dotenv


def zaladuj_env():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    paths = [
        os.path.join(base_dir, '.env'),
        os.path.join(os.path.dirname(base_dir), '.env'),
        os.path.join(os.getcwd(), '.env')
    ]
    for p in paths:
        if os.path.exists(p):
            load_dotenv(p)
            return
    load_dotenv()


zaladuj_env()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "baza_treningowa")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
