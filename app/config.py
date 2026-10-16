import os
import gspread
from google.oauth2.service_account import Credentials

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    MONGODB_SETTINGS = {
        'db': 'game_data',
        'host': 'localhost',
        'port': 27017
    }

    GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '')
    GOOGLE_SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID', '')
    GOOGLE_SHEETS_SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
    ]

    # AI hint configuration
    AI_HINT_ENABLED = os.getenv("AI_HINT_ENABLED", "False")
    AI_HINT_PROVIDER = os.getenv("AI_HINT_PROVIDEER", "none") # none| ollama |openai
    AI_HINT_TIMEOUT_SECONDS = int(os.getenv("AI_HINT_TIMEOUT_SECONDS", "15"))

    # Local Ollama
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

    # External OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-40-mini")

class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
