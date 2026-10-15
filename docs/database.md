# Database

> Note: this document was AI-generated with human review.

This project uses **MongoDB** through **MongoEngine**.

> **Important:** the older SQLite/SQLAlchemy/Alembic database guide from the
> previous version of this project is no longer relevant. The current app does
> not use relational tables or migration files.

## Where the database lives

- **Development:** a local MongoDB instance started with `docker compose up -d`
  and exposed on `localhost:27017`
- **Database name:** `game_data`
- **Primary collection:** `users`

The connection details live in `app/config.py` under `MONGODB_SETTINGS`.

## Starting and stopping the local database

```bash
docker compose up -d
docker compose down
```

The compose file starts the official `mongo` image and mounts a named volume,
so your local data persists between container restarts.

## Inspecting data

You can inspect the database in a few ways:

### From the application shell

```bash
uv run flask shell
>>> from app.models.user import User
>>> User.objects.count()
>>> User.objects.first()
```

### With MongoDB tools

Use MongoDB Compass, the `mongosh` shell, or any MongoDB client pointed at
`mongodb://localhost:27017`.

## How the app reads and writes data

MongoEngine exposes document classes directly. In this project:

- `app/models/user.py` defines the `User` document
- routes and services use `User.objects...` for queries
- `.save()`, `.reload()`, and `.delete()` are the main persistence methods

Example:

```python
from app.models.user import User

user = User(name="Example", domains=["example.com"])
user.save()

existing = User.objects(name="Example").first()
```

## What changed from the old docs

There is **no migration workflow** in the current app and no `flask db`
commands to run. If you see references to `db.create_all()`, Alembic, or
`migrations/versions/`, those belong to the older SQLAlchemy version of the
project and should be ignored here.

Schema changes in this app are handled by changing the MongoEngine document
definition and, if necessary, writing data-migration scripts manually.
