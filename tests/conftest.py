import os
import pytest
import mongomock
import mongoengine as me
from flask import Flask
from app.routes.routes import bp
from app.models.user import User


@pytest.fixture
def app():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(base_dir, "app", "templates")

    app = Flask(__name__, template_folder=template_dir)
    app.register_blueprint(bp)
    app.config.update({
        "TESTING": True,
        "GOOGLE_SPREADSHEET_ID": "dummy_sheet_id_123"
    })
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    with app.test_client() as test_client:
        yield test_client

@pytest.fixture(scope="session", autouse=True)
def mock_mongo_connection():
    """Connect to a mock MongoDB instance for the entire test session."""
    connection = me.connect(
        'mongoenginetest',
        host='mongodb://localhost',
        mongo_client_class=mongomock.MongoClient
    )
    yield connection
    me.disconnect(alias='default')

@pytest.fixture(autouse=True)
def clean_db():
    """Clear the collections before each individual test to ensure isolation."""
    User.drop_collection()
