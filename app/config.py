import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pokemon.db")
API_USERNAME = os.getenv("API_USERNAME", "kauan")
API_PASSWORD = os.getenv("API_PASSWORD", "admin")
