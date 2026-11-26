# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Spendly** — A personal expense tracking web application built with Flask. The project follows a step-by-step implementation guide for students learning web development.

## Commands

### Setup
```bash
# Create virtual environment (already exists)
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Development
```bash
# Run the Flask app (port 5001)
python app.py

# Run tests
pytest
# or for verbose output
pytest -v

# Run a single test file
pytest tests/test_app.py -v
```

### Database
```bash
# Database file: expense_tracker.db (SQLite)
# Schema is initialized in database/db.py
```

## Architecture

### Directory Structure
```
expense-tracker/
├── app.py                 # Main Flask application & routes
├── requirements.txt       # Python dependencies
├── database/
│   ├── __init__.py
│   └── db.py              # Database functions (get_db, init_db, seed_db)
├── static/
│   ├── css/
│   │   └── style.css      # Complete design system
│   └── js/
│       └── main.js        # Vanilla JS (currently empty placeholder)
├── templates/
│   ├── base.html          # Base layout with navbar/footer
│   ├── landing.html       # Landing page with hero, features, modal
│   ├── login.html         # Login form
│   ├── register.html      # Registration form
│   └── terms.html         # Terms & Conditions page
└── venv/                  # Virtual environment (gitignored)
```

### Key Components

**app.py** — Flask app with routes:
- `/` — Landing page (landing.html)
- `/register` — Registration page
- `/login` — Login page
- `/terms` — Terms & Conditions page
- Placeholder routes for `/logout`, `/profile`, `/expenses/*` (Steps 3-9)

**database/db.py** — Student implementation target for:
- `get_db()` — SQLite connection with row_factory & foreign keys
- `init_db()` — Creates tables via CREATE TABLE IF NOT EXISTS
- `seed_db()` — Inserts sample data for development

**templates/base.html** — Base template with:
- Navbar (brand, Sign in, Get started CTA)
- Footer (brand, copyright, Terms & Conditions link to `/terms`, Privacy Policy placeholder `#`)
- Blocks: `title`, `head`, `content`, `scripts`

**static/css/style.css** — Complete design system with:
- CSS custom properties for colors, fonts, spacing
- Components: navbar, hero, mock card, buttons, features, CTA, auth forms, legal pages, modal, footer
- Responsive breakpoints at 900px and 600px

**templates/landing.html** — Landing page with:
- Hero section with badge, title, subtitle, CTA buttons (Create Free Account, See How It Works)
- Mock dashboard card visualization
- Features section (3 cards)
- CTA section
- YouTube video modal (vanilla JS, stops video on close)

---

## Code style

- Python: PEP 8, snake_case for all variables and functions
- Templates: Jinja2 with `url_for()` for every internal link — never hardcode URLs
- Route functions: one responsibility only — fetch data, render template, done
- DB queries: always use parameterized queries (`?` placeholders) — never f-strings in SQL
- Error handling: use `abort()` for HTTP errors, not bare `return "error string"`

---

## Tech constraints

- **Flask only** — no FastAPI, no Django, no other web frameworks
- **SQLite only** — no PostgreSQL, no SQLAlchemy ORM, no external DB
- **Vanilla JS only** — no React, no jQuery, no npm packages
- **No new pip packages** — work within `requirements.txt` as-is unless explicitly told otherwise
- Python 3.10+ assumed — f-strings and `match` statements are fine

---

## Subagent Policy
- Always use a builtin explore subagent for codebase exploration 
  before implementing any new feature
- Always use a subagent to verify test results 
  after any implementation
- When asked to plan, delegate codebase research 
  to a subagent before presenting the plan
- always use a builtin plan subagent in plan mode

---

### Design System (from style.css)
- **Colors**: `--ink` (#0f0f0f), `--accent` (#1a472a), `--accent-2` (#c17f24), `--paper` (#f7f6f3), `--danger` (#c0392b)
- **Fonts**: `--font-display`: 'DM Serif Display', `--font-body`: 'DM Sans'
- **Radius**: `--radius-sm` (6px), `--radius-md` (12px), `--radius-lg` (20px)
- **Max widths**: `--max-width` (1200px), `--auth-width` (440px)



## Development Notes

- Uses SQLite (`expense_tracker.db`) — auto-created on first run
- No authentication implemented yet (Steps 3-9 are placeholders)
- Vanilla JavaScript only — no frameworks
- Templates use Jinja2 inheritance (`{% extends "base.html" %}`)
- Landing page modal uses `data-src` on iframe to stop video on close
- Student implementation steps are marked in code comments


## Implemented vs stub routes

| Route | Status |
|---|---|
| `GET /` | Implemented — renders `landing.html` |
| `GET /register` | Implemented — renders `register.html` |
| `GET /login` | Implemented — renders `login.html` |
| `GET /logout` | Stub — Step 3 |
| `GET /profile` | Stub — Step 4 |
| `GET /expenses/add` | Stub — Step 7 |
| `GET /expenses/<id>/edit` | Stub — Step 8 |
| `GET /expenses/<id>/delete` | Stub — Step 9 |

**Do not implement a stub route unless the active task explicitly targets that step.**

---

## Warnings and things to avoid

- **Never use raw string returns for stub routes** once a step is implemented — always render a template
- **Never hardcode URLs** in templates — always use `url_for()`
- **Never put DB logic in route functions** — it belongs in `database/db.py`
- **Never install new packages** mid-feature without flagging it — keep `requirements.txt` in sync
- **Never use JS frameworks** — the frontend is intentionally vanilla
- **`database/db.py` is currently empty** — do not assume helpers exist until the step that implements them
- **FK enforcement is manual** — SQLite foreign keys are off by default; `get_db()` must run `PRAGMA foreign_keys = ON` on every connection
- The app runs on **port 5001**, not the Flask default 5000 — don't change this