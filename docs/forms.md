# Forms (WTForms)

> Note: this document was AI-generated with human review.

This app uses **WTForms** directly for the data-loading form. `Flask-WTF` is
installed, but CSRF protection is not initialized yet.

> **Important:** older examples in this guide referred to a `PostForm` and a
> SQLAlchemy-backed create/edit workflow. Those examples are no longer
> relevant to the current app.

## What the current form looks like

The form lives in `app/forms.py` and is called `UserForm`:

```python
from wtforms import FieldList, Form, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


def validate_domain_name(form, field):
    ...


class UserForm(Form):
    name = StringField("Enter name of domain owner", [DataRequired()])
    domains = FieldList(StringField("", validators=[validate_domain_name]), min_entries=1)
    submit = SubmitField("Load User")
```

This form is used by the `/load/data` route.

## Why use WTForms here?

The app needs a little structure around user input:

- a person name
- one or more domain names
- validation for each domain value

WTForms keeps that logic in one place instead of spreading it across the route
handler.

## How the current route uses the form

The relevant route in `app/routes/routes.py` builds a `UserForm` from
`request.form` on `POST`, removes the extra blank domain entry, and then calls
`form.validate()` before saving anything.

That means the form is being validated manually with `form.validate()` rather
than `validate_on_submit()`.

## Validation behavior

The current validation rules are:

- `name` is required
- at least one `domains` entry must exist
- every domain must look like a valid domain name and must be reasonably
  short

The custom `validate_domain_name()` helper enforces the domain format.

## Rendering the form in a template

The current template is `app/templates/pages/loaddata.html`. It renders the
fields directly and shows form errors and success messages beneath the form.

That template currently uses a plain HTML form rather than a `FlaskForm`
helper block.

## CSRF status

CSRF protection is **not enabled yet** in this codebase. `flask-wtf` is a
dependency, but `CSRFProtect` is not initialized in `app/extensions.py` or
`app/__init__.py`.

That means:

- the form currently works without a CSRF token
- if CSRF is added later, the template will need a hidden token field
- tests and routes will need to be updated at the same time

## Common mistakes to avoid

- **Assuming Flask-WTF protection is already active.** It is not.
- **Forgetting to validate each list item.** `FieldList` validates the items,
  but your custom validator still needs to be attached to the field.
- **Treating `request.form` as already clean.** The route still has to strip
  empty domains and handle invalid data.
- **Using this old doc as if it described a `PostForm`.** That workflow was
  part of the previous version of the project and no longer applies.
