import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Automatically create the 'db/' folder if it doesn't exist
os.makedirs("app/db", exist_ok=True)


SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY environment variable is not set!")


# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# SQLite database file path (from .env or fallback)
DB_PATH = os.getenv("DB_PATH", "app/db/medicoast.db")

# OpenAI model choice (default: gpt-3.5-turbo)
AI_MODEL = os.getenv("AI_MODEL", "gpt-3.5-turbo")