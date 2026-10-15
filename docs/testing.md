# Testing

> Note: this document was AI-generated with human review.

Tests live in `tests/` and use `pytest`.

Run the full suite with:

```bash
uv run pytest
```

Run one file, or one test, with:

```bash
uv run pytest tests/test_routes.py
uv run pytest tests/test_routes.py::test_home_page
```

Add `-v` for verbose output, or `--cov=app` if you want a coverage report:

```bash
uv run pytest --cov=app --cov-report=term-missing
```

> **Important:** the old testing guide for the earlier SQLAlchemy version of
> this project is no longer relevant. The current suite uses Flask, `mongomock`,
> and manual app setup.

## The fixtures (`tests/conftest.py`)

| Fixture | What it gives you |
|---|---|
| `app` | A Flask app with the main blueprint registered, `TESTING=True`, and a template folder set explicitly |
| `client` | `app.test_client()` for simulating HTTP requests |
| `mock_mongo_connection` | A session-scoped `mongomock` connection for MongoEngine |
| `clean_db` | Drops the `User` collection before each test for isolation |

The current test app is built manually instead of calling `create_app()`, so
the tests can control the template path and MongoEngine connection.

## Testing a route

Use the `client` fixture whenever you are checking HTTP behavior:

```python
def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
```

That keeps the test inside Flask’s real request/response cycle.

## Testing the database layer

The app uses MongoEngine, so tests should work with documents directly:

```python
from app.models.user import User


def test_user_can_be_saved(app):
    user = User(name="Alice", domains=["example.com"])
    user.save()

    assert User.objects.count() == 1
```

The `mongomock` fixture prevents tests from touching a real MongoDB server.

## Mocking service classes when needed

The current route tests patch `DataManager` and `DataGenerator` in
`app.routes.routes`. That is a good pattern when the route’s behavior is what
you want to verify, not the internals of the service object.

Example:

```python
from unittest.mock import patch


def test_fetch_data(client):
    with patch("app.routes.routes.DataGenerator") as mock_data_generator:
        mock_instance = mock_data_generator.return_value
        mock_instance.generate_data.return_value = {"status": "Success"}

        response = client.get("/fetch/data")
        assert response.status_code == 200
```

## What is isolated between tests

Each test gets a fresh `User` collection because `clean_db` drops it before the
test runs. The mocked MongoDB connection is shared for the test session, but
the data does not leak from one test to the next.

## Naming and organization conventions

- Keep one test file per concern: `test_routes.py`, `test_app_factory.py`,
  `test_data_generator.py`, and so on.
- Name tests after behavior, not implementation details.
- Use mocks for external integrations or expensive service calls, but keep
  route tests focused on the observable response.

## Old guidance that no longer applies

- SQLAlchemy session fixtures and `db.create_all()` examples are outdated.
- Alembic / migration-based test setup is not used in this version.
- The old warning about declaring SQLAlchemy models inside test functions no
  longer applies as written here.
