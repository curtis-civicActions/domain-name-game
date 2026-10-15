# Adding a Model

> Note: this document was AI-generated with human review.

In the current app, “model” means a **MongoEngine document**. Documents live
in `app/models/`, and you import them directly where they are needed.

> **Note:** the older SQLAlchemy/Base/migration workflow from earlier project
> versions is obsolete here. There is no `models/__init__.py` registration step
> and no `flask db migrate` command in this version.

## 1. Create a document class

The existing `User` document in `app/models/user.py` is the best example:

```python
import mongoengine as me

from app.extensions import db


def min_items(val):
    if len(val) < 1:
        raise me.ValidationError("List must contain at least 1 item.")


class ExampleUser(db.Document):
    meta = {"collection": "users"}
    name = me.StringField(required=True, max_length=100)
    domains = me.ListField(me.StringField(), validation=min_items)
```

This is the general pattern for MongoEngine documents in this project:

- inherit from `db.Document`
- define fields with `mongoengine` field types
- use helper validators when you need custom rules

## 2. Import the document where it is used

Unlike SQLAlchemy, MongoEngine does not need a special import registry file to
make a document “exist.” If a route or service needs `User`, just import it
directly:

```python
from app.models.user import User
```

That is enough for querying and saving.

## 3. Use MongoEngine methods instead of session-based ORM calls

Examples:

```python
user = ExampleUser(name="Example", domains=["example.com"])
user.save()

ExampleUser.objects(name="Example").first()
ExampleUser.objects.all().delete()
```

The current app uses these patterns in `app/services/datamanager.py` and
`app/services/datagenerator.py`.

## 4. Think about validation early

The app already shows a few useful validation patterns:

- `required=True` on `name`
- `max_length=100` on the owner name
- a custom validator to ensure the `domains` list has at least one item

If you add a new document, add validation there instead of relying only on the
form layer. That keeps invalid data out of the database even if it comes from
another path later.

## Common mistakes to avoid

- **Writing SQLAlchemy-style examples for MongoEngine.** `Mapped[...]`,
  `mapped_column(...)`, `Base`, and `db.session` are not part of this app.
- **Assuming a `models/__init__.py` import is required.** It is not.
- **Skipping validation.** MongoEngine will store what you tell it to store
  unless you validate first.
- **Reusing one document name for multiple concepts.** Keep the model names
  close to the real data shape (`User`, `GameEntry`, `QuestionSet`, etc.).

## When a new document should be added

Add a new document when the app needs a new kind of persistent record — for
example, if you split the game into users, rounds, and answers. If the data is
just a transient calculation or spreadsheet-derived payload, a service object
may be a better fit than a new document class.
