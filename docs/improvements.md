# Possible Improvements / Open Tasks

> Note: this document was AI-generated with human review.

This is a running list of current rough edges and reasonable next steps for
the app. It is intentionally not exhaustive.

> **Historical note:** older items about SQLAlchemy, `Post.slug`, and
> Alembic-based workflows belonged to a previous version of this project and
> are no longer relevant. They have been retired from this backlog.

## Google Sheets import robustness

The app initializes the Google Sheets client at startup, so errors in the
credential path or spreadsheet ID can break the app before the first request
ever reaches a route.

Potential improvements:

- validate the Google credential settings earlier and fail with a clearer
  message
- make the spreadsheet loading route more defensive when the sheet format is
  unexpected
- add better user-facing errors when the spreadsheet cannot be loaded

## CSRF protection

`flask-wtf` is installed, but CSRF protection is not wired into the app yet.
If a future version adds more form-backed routes, it would be a good time to
initialize `CSRFProtect` and update the templates/tests accordingly.

## Data validation and cleanup

The current manual data entry flow could still be hardened:

- reject obviously invalid domain lists earlier
- make duplicate handling more explicit when updating an existing user
- consider stronger normalization for name/domain input

## Testing coverage

The current test suite covers the app factory and the main routes, but there is
room to grow:

- add more direct tests for `DataGenerator`
- add more direct tests for `DataManager`
- cover the domain validator in `app/forms.py`
- add a few route tests for failure paths and malformed input

## UI and interaction polish

The current templates are intentionally simple. Future improvements could
include:

- clearer success/error messaging on the data-loading page
- better empty-state handling on the game screen
- more accessible controls and labels in the interactive views

## What is intentionally left lightweight

This project is meant to stay easy to understand. Things like user accounts,
admin dashboards, and a heavier front-end framework are still out of scope for
now unless the project grows enough to justify them.
