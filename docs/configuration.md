# Configuration

> Note: this document was AI-generated with human review.

This project uses two layers of configuration:

1. Flask CLI bootstrapping via `.flaskenv`
2. Application settings in `app/config.py`

They serve different purposes and should not be mixed together.

## `.flaskenv` — Flask CLI bootstrapping

Current contents:

```bash
FLASK_APP=app.app
FLASK_DEBUG=1
```

- Tells the `flask` CLI where to find the app before it can run commands like
  `flask run`, `flask shell`, or `flask routes`.
- Is committed to git because it is not secret data — it is just local run
  configuration.
- Only affects the `flask` CLI. If you start the app some other way, this file
  is not used.

## `.env` — local secrets and environment-specific values

This repository does not currently include a checked-in `.env` file, but the
app will read environment variables if you set them locally. The important
values are:

- `GOOGLE_APPLICATION_CREDENTIALS` — path to the Google service-account JSON
- `GOOGLE_SPREADSHEET_ID` — the sheet the app loads data from when using the
  spreadsheet import path

If you add more environment-dependent settings later, this is the right place
to document them. Do **not** commit real secrets.

## `app/config.py` — the application config classes

The current config file defines these values:

```python
import os

class Config:
    MONGODB_SETTINGS = {
        "db": "game_data",
        "host": "localhost",
        "port": 27017,
    }

    GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    GOOGLE_SPREADSHEET_ID = os.getenv("GOOGLE_SPREADSHEET_ID", "")
    GOOGLE_SHEETS_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
```

`create_app(config_name)` picks one of these classes from the `config` mapping:

- `development`
- `testing`
- `production`
- `default` (currently development)

Development enables debug mode, testing enables Flask’s test flag, and
production disables debug mode.

## What to add when the app needs a new setting

1. Add the setting to `Config` or a specific subclass in `app/config.py`.
2. Read it from the environment with `os.getenv(...)` if it should be set
   externally.
3. Access it through `current_app.config[...]` or `app.config[...]`.

## Notes on the current version

- There is **no `SQLALCHEMY_DATABASE_URI`** in this project anymore.
- There is **no `SECRET_KEY` setting yet**. If CSRF protection or signed
  sessions are added later, that will need to be introduced.
- If you want a teammate to run the app easily, consider adding a simple
  `.env.example` with the required Google environment variables.
