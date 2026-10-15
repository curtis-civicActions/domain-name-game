from app.config import DevelopmentConfig, ProductionConfig, TestingConfig


def test_create_app_defaults_to_development(monkeypatch):
    monkeypatch.delenv("FLASK_ENV", raising=False)
    from app import create_app

    app = create_app()
    assert app.config["DEBUG"] is DevelopmentConfig.DEBUG


def test_testing_config_uses_mongodb_settings():
    # This project does not use an in-memory SQLite database. The testing
    # config only flips Flask into test mode and keeps the MongoDB settings
    # aligned with the app's local Mongo connection.
    assert TestingConfig.TESTING is True
    assert TestingConfig.MONGODB_SETTINGS == {
        "db": "game_data",
        "host": "localhost",
        "port": 27017,
    }


def test_production_config_disables_debug():
    from app import create_app

    app = create_app("production")
    assert app.config["DEBUG"] is ProductionConfig.DEBUG


def test_instance_folder_is_created(app):
    import os

    assert os.path.isdir(app.instance_path)
