# Flask Basics

> Note: this README was AI-generated with human review.

A small Flask application centered on a domain-name game. The app lets you
load people/domain pairs manually or from Google Sheets, store them in
MongoDB, and turn that data into a simple “who owns this domain?” quiz.
The README and linked docs are meant to explain not just *what* to run, but
*why* the project is structured the way it is.

This project is a good place to learn or practice:

- **Flask fundamentals**: request/response flow, blueprints, templates, and
  Flask’s extension pattern.
- **MongoEngine + MongoDB**: document modeling, querying, and local database
  setup.
- **Forms and validation**: WTForms-driven input handling for the manual data
  loader.
- **Spreadsheet integration**: pulling data from Google Sheets with a service
  account.
- **Server-rendered UI with light interactivity**: Jinja2 templates, HTMX,
  and a small amount of custom JavaScript.

## Stack

- **[Flask](https://flask.palletsprojects.com/)** — web framework and app factory
- **[MongoEngine](https://mongoengine.org/)** — document modeling for MongoDB
- **[MongoDB](https://www.mongodb.com/)** — local data store, started via Docker Compose
- **[WTForms](https://wtforms.readthedocs.io/)** / **[Flask-WTF](https://flask-wtf.readthedocs.io/)** — form handling and validation building blocks
- **[gspread](https://docs.gspread.org/)** + **Google auth libraries** — Google Sheets import via service account credentials
- **[Faker](https://faker.readthedocs.io/)** — generate sample names and domains
- **[HTMX](https://htmx.org/)** — partial page updates without a full SPA
- **[Tailwind CSS](https://tailwindcss.com/)** — utility-first styling via the CDN build
- **[pytest](https://docs.pytest.org/)** + **mongomock** — automated tests with a mocked MongoDB backend
- **[uv](https://docs.astral.sh/uv/)** — dependency management and command runner

If you do not know one of these tools yet, that is fine — this repo is a
learning project, so the expectation is to look things up as you go.

## Quick start

**Prerequisites:** [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
and Docker/Compose. You also need a Google service-account JSON file and a
spreadsheet ID if you want the spreadsheet import features to work, because
the app initializes that client on startup.

```bash
# Install dependencies (creates .venv/ automatically)
uv sync

# Start MongoDB locally
docker compose up -d

# Make sure the app can find your Google credentials and spreadsheet
# export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
# export GOOGLE_SPREADSHEET_ID=<your-sheet-id>

# Run the dev server
uv run flask run

# Or start MongoDB + wait for it + launch Flask in one go
./startapp.sh

# Run the tests
uv run pytest
```

Every command in this repo is run through `uv` instead of activating a
virtual environment manually. `uv run` uses the project’s `.venv`
automatically.

### Useful commands

```bash
uv run flask routes        # list every registered route
uv run flask shell         # open a Python shell with app context loaded
uv run flask run           # start the dev server
uv run pytest              # run the test suite
uv run pytest -v           # verbose test output
uv run pytest tests/test_routes.py   # run one test file
docker compose up -d       # start MongoDB
docker compose down        # stop MongoDB
uv run pre-commit install  # install the repo hooks once
```

## Project structure

```
.
├── app/
│   ├── __init__.py        # create_app() factory + app-wide context setup
│   ├── app.py             # thin entrypoint: app = create_app()
│   ├── config.py          # development / testing / production config
│   ├── extensions.py      # MongoEngine connection + Google Sheets client
│   ├── forms.py           # WTForms form and custom validators
│   ├── models/            # MongoEngine documents
│   ├── routes/            # main blueprint and page/data routes
│   ├── services/          # spreadsheet loading, sample-data generation, persistence helpers
│   ├── static/            # JavaScript, CSS, favicon, and images
│   └── templates/         # Jinja base layout, pages, and partials
├── tests/                 # pytest suite and fixtures
├── docker-compose.yml     # local MongoDB service
├── instance/              # runtime files created locally
├── startapp.sh            # convenience script to start the app stack
├── .flaskenv              # Flask CLI bootstrap (FLASK_APP, debug)
├── game-data-creds.json   # local Google service-account credentials file
├── pyproject.toml
└── docs/                  # deeper guides and notes
```

## Documentation

This README covers the basics. For deeper context, see the guides in
`docs/`:

| Guide | What’s in it |
|---|---|
| [`docs/architecture.md`](docs/architecture.md) | How the app factory, blueprints, extensions, and request flow fit together |
| [`docs/configuration.md`](docs/configuration.md) | `.flaskenv`, `.env`, and `app/config.py` |
| [`docs/database.md`](docs/database.md) | Local database setup, Docker, and persistence workflow |
| [`docs/forms.md`](docs/forms.md) | Form handling, validation, and request processing |
| [`docs/templates.md`](docs/templates.md) | Jinja layout, partials, and page composition |
| [`docs/adding-routes.md`](docs/adding-routes.md) | How to add or organize routes with blueprints |
| [`docs/adding-models.md`](docs/adding-models.md) | How to add or register data models/documents |
| [`docs/testing.md`](docs/testing.md) | Pytest fixtures, client usage, and test isolation |
| [`docs/improvements.md`](docs/improvements.md) | Known gaps, rough edges, and next-step ideas |

**If you only read one doc, read `docs/architecture.md` first** — it explains
the factory/blueprint setup that everything else builds on.

## Contributing / making changes

Rough workflow for adding a feature end to end:

1. Update or add the data model/document in `app/models/`.
2. Update the relevant service or form code in `app/services/` or `app/forms.py`.
3. Add or adjust the route in `app/routes/routes.py`.
4. Update the matching template in `app/templates/`.
5. Add or update tests in `tests/`.
6. Run `uv run pytest` before considering the change done.

Before committing your work, run `uv run pre-commit install` once. After
that, the hooks in [`.pre-commit-config.yaml`](.pre-commit-config.yaml) run
automatically on every commit: [Ruff](https://docs.astral.sh/ruff/) (lint and
format), [mypy](https://mypy-lang.org/) (type checking),
[Bandit](https://bandit.readthedocs.io/en/latest/) (security linting),
[Commitizen](https://commitizen-tools.github.io/commitizen/) (commit message
formatting), and a few general file checks.

## Commit messages: Commitizen + Conventional Commits

This repo enforces [Conventional Commits](https://www.conventionalcommits.org/)
via the `commit-msg` hook. Once you have run `pre-commit install`, any commit
message that does not match the required format is rejected:

```text
<type>(<optional scope>): <description>
```

Allowed `<type>` values include `feat`, `fix`, `build`, `bump`, `chore`,
`ci`, `docs`, `perf`, `refactor`, `revert`, `style`, and `test`.

```bash
git commit -m "feat: add spreadsheet import support"
git commit -m "fix(routes): handle empty domain lists"
git commit -m "not following the format"   # rejected by the commit-msg hook
```

If you would rather not memorize the format, use Commitizen’s interactive
prompt instead of `git commit` directly:

```bash
uv run cz commit
```

Why this matters beyond style: Conventional Commits makes changelog
generation and semantic versioning easier later. The commit history becomes
structured data instead of free text.

## Known gaps / honest state of this project

This is a real working app, not a polished product. A few things are still
intentionally rough or incomplete:

- **Google credentials are required at startup.** `create_app()` initializes
  the Google Sheets client immediately, so the app will not boot cleanly
  without a valid `GOOGLE_APPLICATION_CREDENTIALS` value.
- **The data-loading flow assumes a fairly specific spreadsheet shape.** If
  the sheet does not match what `DataGenerator` expects, you will need to
  adjust the loader.
- **Some route/service logic is still intentionally lightweight.** The app is
  built for experimentation and learning, so there is no admin dashboard,
  authentication system, or polished CRUD interface yet.
- **The UI is intentionally minimal.** Tailwind and HTMX keep the pages simple
  and fast to iterate on, but the front end is still a prototype rather than a
  finished product.

If you want to extend this project, the next natural steps are usually a real
admin workflow for entering data, better validation around the spreadsheet
import, and more complete error handling around external services.
