# Architecture

> Note: this document was AI-generated with human review.

This app uses the **application factory** pattern with a single **blueprint**
for the main site routes. That is the right shape for a Flask app that needs
to be testable, configurable, and able to grow beyond a tiny script.

> **Note:** older SQLAlchemy/Alembic-era guidance from previous versions of
> this project is no longer relevant. The current app uses MongoEngine and
> MongoDB instead.

## Why a factory instead of a global `app = Flask(__name__)`?

The simple tutorial pattern works for a throwaway demo, but it quickly gets in
the way here because:

1. **Tests need their own app instance.** The test suite uses a special
   configuration and a mocked MongoDB connection.
2. **Extensions must be initialized cleanly.** The database client and Google
   Sheets client are bound inside the factory instead of being created at
   import time.
3. **Routes should not be assembled until the app exists.** Import order stays
   predictable when the app is built in one place.

In this project, the factory lives in `app/__init__.py`. It:

- reads the active config name from `FLASK_ENV` or the caller
- creates the Flask app with `instance_relative_config=True`
- loads the matching config class from `app.config.config`
- ensures the instance directory exists
- initializes MongoEngine with `db.init_app(app)`
- initializes the Google Sheets client
- imports and registers the `main` blueprint from `app.routes`

Anything that needs an app — the dev server, tests, a future CLI, or a WSGI
server — calls `create_app()` and gets a configured instance back.

## The moving pieces

```
app/
├── __init__.py        # create_app() factory and app-wide setup
├── app.py             # thin entrypoint: app = create_app()
├── config.py          # development/testing/production config classes
├── extensions.py      # MongoEngine connection and Google Sheets client
├── forms.py           # WTForms definitions and validators
├── models/            # MongoEngine documents
├── routes/            # the main blueprint and page routes
├── services/          # data loading, sample generation, persistence helpers
├── static/            # JS, CSS, favicon, images
└── templates/         # base layout, page templates, and partials
```

### `config.py`

`app/config.py` defines plain configuration classes and a `config` mapping.
`create_app(config_name)` picks one by name (`development`, `testing`,
`production`, or `default`). The current configuration includes:

- `MONGODB_SETTINGS` for MongoEngine
- `GOOGLE_CREDENTIALS_PATH` and `GOOGLE_SPREADSHEET_ID`
- `GOOGLE_SHEETS_SCOPES`

See [`configuration.md`](configuration.md) for the environment-variable side
of that setup.

### `extensions.py`

This file creates the shared extension objects without attaching them to an
app immediately:

```python
from flask_mongoengine import MongoEngine

db = MongoEngine()
```

The MongoDB client is bound later in `create_app()` with `db.init_app(app)`.
The same pattern is used for the Google Sheets client in
`init_google_service_client(app)`.

This “create it once, bind it later” approach avoids circular imports and is
the standard Flask extension pattern.

### `routes/` (blueprints)

The current app has one blueprint, `main`, defined in `app/routes/routes.py`.
It handles:

- landing and informational pages (`/`, `/about`, `/start`, `/gather/data`)
- HTMX partial loading (`/get-partial/question/<view_name>`)
- spreadsheet/database loading routes (`/fetch/data`, `/load/data`)
- field validation (`/validate-field`)

If this project grows, new feature areas should still be split into their own
blueprints rather than adding more and more handlers to one file.

### `app.py`

This file is just the launch point:

```python
from app import create_app

app = create_app()
```

It exists so the Flask CLI and a WSGI server have a simple module-level app
to point at.

## Request lifecycle, in one sentence

`create_app()` builds the app → a browser request hits one of the blueprint
routes → the route uses MongoEngine documents or a service class like
`DataManager`/`DataGenerator` → the route renders a Jinja template or returns
JSON → Flask sends the response.

There are no SQLAlchemy sessions or Alembic migrations in this version of the
project. The old migration workflow is historical only.
