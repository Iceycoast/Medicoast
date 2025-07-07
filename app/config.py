import os
from dotenv import load_dotenv

# Automatically create the 'db/' folder if it doesn't exist
os.makedirs("app/db", exist_ok=True)

# Load environment variables from .env
load_dotenv()

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# SQLite database file path (from .env or fallback)
DB_PATH = os.getenv("DB_PATH", "app/db/medicoast.db")

# OpenAI model choice (default: gpt-3.5-turbo)
AI_MODEL = os.getenv("AI_MODEL", "gpt-3.5-turbo")
