# Templates

> Note: this document was AI-generated with human review.

Templates live in `app/templates/` and use Jinja2. Styling is handled with
[Tailwind CSS](https://tailwindcss.com/) via the CDN build, so there is no
Node/npm build step in the current project.

```
app/templates/
├── base.html
├── index.html
├── pages/
│   ├── home.html
│   ├── about.html
│   ├── start.html
│   ├── gather.html
│   └── loaddata.html
└── partials/
    ├── nav.html
    ├── footer.html
    └── question.html
```

## `base.html` — the site-wide layout

`base.html` is the shared skeleton for the app. It defines the page shell,
loads Tailwind, loads the HTMX script, includes the nav and footer, and gives
child templates the following blocks:

| Block | Purpose |
|---|---|
| `title` | `<title>` tag content |
| `head` | Extra `<head>` content for page-specific scripts |
| `content` | Main body of the page |
| `scripts` | Extra scripts at the bottom of the page |

Use `base.html` directly when the page needs forms, HTMX behavior, or more
custom layout control.

## `index.html` — the wrapper for simple content pages

`index.html` extends `base.html` and adds a consistent heading plus a reading
width container. Static pages like `home.html` and `about.html` extend this
template.

Example usage:

```jinja
{% extends "index.html" %}
{% set page_title = "About" %}

{% block page_content %}
<p>About content here.</p>
{% endblock %}
```

Use `index.html` for simple pages that do not need their own full page layout.

## `partials/nav.html` and `partials/footer.html`

These are reusable fragments included from `base.html`.

- `nav.html` contains the current top navigation links (`Home`, `About`)
- `footer.html` shows the current year and the project footer text

Always use `url_for(...)` in these partials so links stay correct if a route
changes.

The footer uses `current_year`, which is injected into every template by the
`context_processor` in `app/__init__.py`.

## `partials/question.html`

This is the HTMX-loaded question block returned by `/get-partial/question/<view_name>`.
It renders either:

- an error message when no question data is available, or
- the current question and its choices

This file is intentionally standalone because it is loaded into the `start`
page dynamically.

## Current page templates

- `home.html` — landing page with links into the app
- `about.html` — simple informational page
- `start.html` — interactive game screen with an HTMX request button
- `gather.html` — data-loading entry page
- `loaddata.html` — WTForms-based manual data entry page

### Template selection rule of thumb

- **Simple page** → extend `index.html`
- **Interactive page or form page** → extend `base.html`

## Tailwind CSS in the current setup

Tailwind is loaded with the CDN script tag in `base.html`. That is fine for a
small learning project, but it is not the recommended production approach for
a larger site.

If the project ever grows enough to need a real CSS build step, switch to a
compiled Tailwind output file and keep the template structure the same.

## `app/static/css/custom.css`

`custom.css` is linked from `base.html` and is available for any styles that
do not fit cleanly into Tailwind utilities.

## No longer relevant guidance from older docs

Older examples in this file referenced pages and models that no longer exist
in the current app. The current template tree above is the authoritative one.
