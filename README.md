# 🦆 Snip — URL Shortener

> A beginner-friendly URL shortener built with **Duck Framework**.  
> Pure Python. No JavaScript. Real-time UI powered by Lively.

**[▶ Try the Live Demo](https://snip-f7eb7528a803.herokuapp.com/)**

---

## What is this?

Snip is a simple web app that turns long, ugly URLs into short clean links.

You paste a URL → click Shorten → get a short link you can share.

It was built to demonstrate how **Duck Framework** works in a real project — forms, real-time UI updates, database storage, and redirects — all in pure Python.

---

## What you will learn from this project

- How a Duck project is structured
- How to build interactive UI components using Lively (no JavaScript needed)
- How to use Django's database (ORM) inside a Duck project without enabling full Django mode
- How forms work in Duck using the `Form` component
- How to handle URL routing and redirects in Duck

---

## Before you start — what you need to know

### What is Duck Framework?

Duck is a Python web framework that lets you build full web applications — including interactive, real-time UIs — without writing any JavaScript. The part that handles real-time updates is called **Lively**.

Think of it like this: instead of writing JavaScript to make a button do something, you write a Python function. Duck takes care of sending the update to the browser for you over a WebSocket connection.

### What is Lively?

Lively is Duck's built-in real-time UI engine. When you click the "Shorten" button in this app, Lively sends the event to the server, runs your Python handler, and updates only the parts of the page that changed — all without reloading the page.

### What is Django doing here?

Django is only being used for **one thing** — its database engine (the ORM). It handles creating and querying the SQLite database that stores your shortened URLs.

> ⚠️ **Important:** You do NOT need to set `USE_DJANGO = True` in `web/settings.py`.  
> `USE_DJANGO` tells Duck to run Django as a full backend server and proxy requests to it.  
> That is not what we are doing here. We are only borrowing Django's database layer.  
> Duck itself serves all the pages and handles all the requests.

---

## Project structure

```
url-shortener/
├── web/
│   ├── main.py                          # Starts the Duck server
│   ├── settings.py                      # Duck configuration
│   ├── urls.py                          # URL routes (/, /s/<code>)
│   ├── views.py                         # Page and redirect views
│   │
│   ├── ui/
│   │   ├── components/
│   │   │   ├── shorten_form.py          # The form with input + button + result
│   │   │   └── stats_bar.py             # Live stats (total links, total clicks)
│   │   └── pages/
│   │       └── home.py                  # The homepage
│   │
│   └── backend/
│       └── django/
│           └── duckapp/
│               ├── core/
│               │   └── models.py        # ShortURL database model
│               └── duckapp/
│                   └── settings.py      # Django database configuration
│
└── etc/
    └── ssl/                             # SSL certificates (for HTTPS)
```

### The key files explained

| File | What it does |
|---|---|
| `web/main.py` | Entry point — runs the Duck server |
| `web/settings.py` | Duck settings — port, debug mode, blueprints etc. |
| `web/urls.py` | Registers the two routes: `/` and `/s/<short_code>` |
| `web/views.py` | `home()` renders the page, `redirect_short_url()` handles redirects |
| `web/ui/pages/home.py` | Builds the full homepage layout |
| `web/ui/components/shorten_form.py` | The interactive form component |
| `web/ui/components/stats_bar.py` | Live counters for total links and clicks |
| `web/backend/django/duckapp/core/models.py` | The `ShortURL` database model |

---

## Installation

### Step 1 — Make sure you have Python 3.10 or newer

```bash
python --version
```

You should see something like `Python 3.10.x` or higher. If not, download Python from [python.org](https://www.python.org/downloads/).

### Step 2 — Install Duck Framework

```bash
pip install duckframework
```

> Duck Framework includes everything you need to run the server.  
> Django is needed here only for the database. Don't worry about installation, Django is installed automatically when Duck is installed.

### Step 3 — Go into the project folder

You need to have the project locally on your machine. You can do this by cloning the project (or just downloading the project).  

**Use the following command to clone the project:
**

```python
git clone https://github.com/duckframework/url-shortener.git
```

Next, navigate to the project:
```bash
cd url-shortener
```

Make sure you are inside the `url-shortener` folder (the one that contains `web/`) before running any commands.

---

## Running the app

### Step 1 — Create the database

Before running the app for the first time, you need to create the database tables. Run these two commands from inside the `url-shortener` folder:

```bash
duck django makemigrations core
duck django migrate
```

> **What just happened?**  
> `makemigrations core` told Django to look at `web/backend/django/duckapp/core/models.py` and generate instructions for creating the database table.  
> `migrate` actually created the table in the SQLite database file (`db.sqlite3`).

### Step 2 — Start the server

Inside the project, run:

```bash
python web/main.py
```

Or alternatively:

```bash
duck runserver
```

### Step 3 — Open the app

Open your browser and go to:

```
http://localhost:8000
```

You should see the Snip homepage. Paste any URL into the input and click **Shorten**.

---

## How it works — step by step

### Shortening a URL

1. You type a URL into the input field and click **Shorten**
2. Duck's Lively system sends the form data to the server over a WebSocket — no page reload
3. The `handle_shorten` method in `ShortenForm` runs on the server:
   - It validates the URL format
   - Creates a new `ShortURL` record in the database with a random 6-character code
   - Builds the full short URL using `resolve("home")`
4. Lively updates the result box and stats bar live in the browser

### Visiting a short URL

When someone visits `http://localhost:8000/s/aB3xZ9`:

1. Duck matches the route `/s/<short_code>` in `web/urls.py`
2. `redirect_short_url()` in `views.py` looks up `aB3xZ9` in the database
3. It increments the click counter atomically
4. It redirects the visitor to the original URL

### The stats bar

The stats bar at the top shows total links shortened and total clicks across all URLs. Every time you shorten a URL, the stats bar refreshes automatically — Lively patches only the number text, nothing else on the page changes.

---

## DEPLOYMENT

Right now short URLs look like `http://localhost:8000/s/aB3xZ9`.

When you deploy this to a real server, update the environment variable like `DEBUG`, `DOMAIN` & `PORT`.  

By default, the `web/main.py` is dynamic, meaning, it can run in production environments. To enter production mode, just set the environment variable `DEBUG` to nothing. 

> Use file `deploy.sh` for easy deployment.

> **Note:** In this project the base URL is actually resolved dynamically using `resolve("home")` in `shorten_form.py`. If you need to override the domain explicitly, update the `handle_shorten` method in `web/ui/components/shorten_form.py`.

---

## Common problems and fixes

### "No such table: core_shorturl"

You haven't run the migrations yet. Run these commands:

```bash
duck django makemigrations core
duck django migrate
```

### "No module named 'duckframework'"

Duck is not installed. Run:

```bash
pip install duckframework
```

### Migrations folder was not created

This usually means Django cannot find the `core` app. Check that `INSTALLED_APPS` in `web/backend/django/duckapp/duckapp/settings.py` contains exactly:

```python
"web.backend.django.duckapp.core",
```

Also make sure you are running `makemigrations core` (with the app name) and not just `makemigrations`.

### Port 8000 is already in use

Another program is using port 8000. Either stop that program, or change the port in `web/main.py`:

```python
app = App(port=8080, addr="0.0.0.0", domain="localhost")
```

---

## Key things to remember about Duck

- **Pages** extend `Page` (or a base page class). You build the layout in `on_create()` and always call `super().on_create()` first.
- **Components** work the same way — extend a component, override `on_create()`, call `super()`, build your children.
- **Lively event binding** uses `.bind("event", handler, update_targets=[...])`. The `update_targets` list tells Duck which components to re-render after the handler runs.
- **Forms** use the `Form` component. Bind to the `submit` event and your handler receives `form_inputs` as a dict. Give each input a `name=` prop so it appears in that dict.
- **Routing** uses `path()` and `re_path()` in `web/urls.py`. Duck supports `<param>` converters directly in `path()`.
- **Shortcuts** — use `duck.shortcuts` for common operations: `to_response()`, `redirect()`, `not_found404()`, `resolve()`, `static()`.

---

## Built with

- [Duck Framework](https://duckframework.xyz) — Python web framework with reactive UI
- [Django ORM](https://docs.djangoproject.com/en/stable/topics/db/) — database layer only
- SQLite — lightweight database, no setup required

---

*This project is part of the Duck Framework showcase. See more at [duckframework.xyz](https://duckframework.xyz).*
