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
    GOOGLE_SHEETS_SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
    ]
    GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'gamecreds.json')
    GOOGLE_SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID', '1r5_223bpUkyx38m8cvy-pt8bBUE0Mln_jG1GaXt14DE')
    #CLIENT = gspread.authorize(CREDS)


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
