# Adding a Route

> Note: this document was AI-generated with human review.

Routes in this app live on a single **blueprint** named `main`, defined in
`app/routes/routes.py`.

> **Note:** the older route examples that referenced a different package
> layout are no longer relevant. The current project keeps its routes in
> `app/routes/routes.py`.

## Adding a route to the existing blueprint

The pattern is simple:

```python
from flask import Blueprint, render_template

bp = Blueprint("main", __name__)


@bp.route("/about")
def about():
    return render_template("pages/about.html")
```

That route is automatically active because `create_app()` registers `bp`
once during app startup.

### A few current examples from the app

- `@bp.route("/")` → home page
- `@bp.route("/start")` → the HTMX game screen
- `@bp.route("/gather/data")` → the data entry / spreadsheet loading page
- `@bp.route("/get-partial/question/<view_name>")` → returns the question
  partial that gets swapped into the page
- `@bp.route("/load/data", methods=["GET", "POST"])` → processes the
  WTForms form

## Adding a new page route

If you want a new static page, add a route that renders a template. In
practice, that means adding a function in `app/routes/routes.py` that returns
`render_template("pages/help.html")` for the new path.

Then create the template under `app/templates/pages/`.

## Adding a route that returns JSON

The app already has one example in `/fetch/data`, which returns JSON instead
of HTML. The route simply returns a dictionary with `success` and `message`
keys, and Flask serializes it as JSON automatically.

Returning a dict makes Flask serialize it as JSON automatically.

## When to create a new blueprint

Keep using the `main` blueprint until the route group starts feeling too big.
If you add a separate feature area later, create a new blueprint package and
register it in `create_app()`.

The pattern looks like this:

```python
from flask import Blueprint

bp = Blueprint("reports", __name__, url_prefix="/reports")
```

Then import that blueprint in `app/__init__.py` and register it there.

## Why the import happens after the blueprint is created

If a routes module imports a blueprint before the blueprint exists, you get a
circular import. The fix is the standard Flask pattern:

1. create `bp`
2. define routes on it
3. import the module from `create_app()`

That is why the blueprint is built before `create_app()` imports it.

## Testing a route

Use the `client` fixture from `tests/conftest.py`:

```python
def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
```

For routes with mocked services, patch `DataManager` or `DataGenerator` in
the route module, as the current tests do.

## Rendering HTML instead of JSON

Most routes in this app render templates. Use `render_template(...)` for
pages, and use JSON only when the front end needs structured data. Static
pages should extend `index.html`; interactive pages like `start.html` and
`loaddata.html` extend `base.html` directly.
