# Spec: Registration

## Overview

Implement the user registration flow so new users can create a Spendly account. The GET `/register` route already renders the registration form template. This step adds the POST handler to process form submissions, validate input, hash passwords with `werkzeug`, insert the new user into the database, show success message and redirect to `/login` on success. Duplicate emails are caught and displayed as inline errors. This completes Step 2 of the Spendly roadmap and establishes the auth foundation for Step 3 (Login/Logout).

## Depends on

- Step 1 (Database Setup) — `users` table exists with `email` UNIQUE constraint, `get_db()`, `init_db()`, `seed_db()` are implemented, and `werkzeug.security.generate_password_hash` is available.

## Routes

- `GET /register` — renders `register.html` (already implemented)
- `POST /register` — processes registration form — **public**

## Database changes

No database changes. The `users` table schema from Step 1 already supports registration:
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `name` TEXT NOT NULL
- `email` TEXT UNIQUE NOT NULL
- `password_hash` TEXT NOT NULL
- `created_at` TEXT DEFAULT (datetime('now'))

## Templates

- **Modify:** `templates/register.html` — add CSRF protection hidden field (optional for now, but form already has proper structure), ensure error display works with `{{ error }}` variable passed from route

## Files to change

- `app.py` — add POST `/register` route handler, import `generate_password_hash` from `werkzeug.security`, import `get_db` from `database.db`
- `templates/register.html` — verify error handling works (already has `{% if error %}` block)

## Files to create

- None

## New dependencies

No new dependencies. Uses existing:
- `sqlite3` (standard library)
- `werkzeug.security` (already in requirements.txt for `generate_password_hash`, `check_password_hash`)

## Rules for implementation

- No SQLAlchemy or ORMs
- Parameterised queries only — never f-strings in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`
- `app.secret_key` must be set in `app.py` for `flash()` to work (use a hardcoded dev string for now)
- Server-side validation must check:
  1. All fields are non-empty
  2. `password == confirm_password`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Route functions: one responsibility only — fetch data, render template, done
- DB queries: always use parameterized queries (`?` placeholders)
- Error handling: use `abort()` for HTTP errors, not bare `return "error string"`
- Never hardcode URLs in templates — always use `url_for()`
- Never put DB logic in route functions — keep it in `database/db.py` (add helper if needed)

## Definition of done
s/
- [ ] `POST /register` route exists in `app.py`
- [ ] Form submission validates: name, email, password all present
- [ ] Password minimum 8 characters enforced (server-side)
- [ ] Email format validated (basic check)
- [ ] Password hashed with `generate_password_hash` before storage
- [ ] New user inserted into `users` table with parameterized query
- [ ] Duplicate email caught (UNIQUE constraint) → re-render form with error message
- [ ] Successful registration redirects to `/login` (using `url_for('login')`)
- [ ] Error messages display in `register.html` via `{{ error }}` template variable
- [ ] App starts without errors
- [ ] Manual test: register new user → redirected to login → user exists in DB
- [ ] Manual test: register duplicate email → shows error on form