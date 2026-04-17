# cryptid_api

A REST API for managing cryptid (legendary creature) records, built with FastAPI and SQLAlchemy. This project is intended to demonstrate how a Python-based API is structured, how HTTP methods map to database operations, and how modern Python tooling works together.

## What is a REST API?

A REST API (Representational State Transfer) is a way for applications to communicate over HTTP. Instead of returning web pages, a REST API returns data — typically JSON — that other applications (a frontend, a mobile app, another service) can consume.

REST APIs are organized around **resources** — the things your application manages. In this project, the resource is a `cryptid`. Operations on that resource are expressed using standard HTTP methods:

<div align="center">

| Method | What it does |
|---|---|
| `GET` | Read one or more records |
| `POST` | Create a new record |
| `PUT` | Update an existing record |
| `DELETE` | Remove a record |

</div>

These operations map directly to **CRUD** — Create, Read, Update, Delete — the four fundamental database operations you've already worked with.

## What's in here

```
cryptid-api/
├── app/
│   ├── main.py          # App setup, middleware, router registration
│   ├── database.py      # Database engine and session configuration
│   ├── models.py        # SQLAlchemy ORM model (maps to the DB table)
│   ├── schemas.py       # Pydantic schemas (shapes of request/response data)
│   └── routers/
│       └── cryptids.py  # Route handlers for all /cryptids endpoints
├── tests/
│   └── test_cryptids.py # Automated tests using an in-memory database
├── scripts/
│   └── populate_db.py   # Seeds the database with sample data
└── pyproject.toml       # Project metadata and dependencies
```

### Key concepts by file

**`models.py`** defines what the database table looks like using SQLAlchemy's ORM. A Python class represents a table, and class attributes represent columns. You never write `CREATE TABLE` — SQLAlchemy handles that.

**`schemas.py`** defines what data looks like going *into* and coming *out of* the API using Pydantic. These are separate from the database models on purpose: what you store in a database and what you expose over an API aren't always the same thing. For example, `CryptidResponse` includes `id` (which the database generates) but `CryptidCreate` does not (because the client shouldn't be sending an ID when creating a record).

**`routers/cryptids.py`** contains all the route handlers — the functions that run when a request hits a specific URL. Using a router keeps `main.py` clean and makes it easy to add new resource types later.

**`main.py`** creates the FastAPI app, registers middleware (like CORS), and connects the router. It also defines the `start()` function that launches the server.

## What is FastAPI?

FastAPI is a Python web framework for building APIs. It uses Python type hints to automatically validate incoming request data, serialize outgoing responses, and generate interactive documentation. When the server is running, you can visit `http://localhost:8000/docs` to see and test all available endpoints in your browser — no separate tool needed.

## What is Uvicorn?

Uvicorn is an **ASGI server** — it's the program that actually listens for incoming HTTP connections and hands them off to your FastAPI app. The relationship is similar to how Apache or IIS sits in front of a web application: FastAPI defines the logic, Uvicorn handles the networking.

When you run `uv run dev`, the `start()` function in `main.py` launches Uvicorn with `reload=True`, which means the server automatically restarts whenever you save a `.py` file. This is useful during development.

## What is uv?

## What is uv?

`uv` is a modern Python package manager — it replaces `pip` and `venv` for managing dependencies and virtual environments. It reads your project's dependencies from `pyproject.toml` and installs them into an isolated `.venv` folder so they don't interfere with other Python projects on your machine.

One of uv's more useful features is that it can also manage Python versions for you. If you don't have Python 3.14 installed, uv can download and install it without affecting any other Python installation on your system:

```bash
uv python install 3.14
```

To see which Python versions you currently have available:

```bash
uv python list
```

When you run `uv sync` inside this project, uv will read the `requires-python = ">=3.14"` line in `pyproject.toml` and automatically use a compatible version — downloading one if necessary. You generally don't need to manually manage which Python version is active; uv handles it per-project.

> [!IMPORTANT]
> If you already have Python installed through python.org, the Microsoft Store, or Homebrew, uv will detect it. You only need to run `uv python install` if no compatible version is found.
> 
## What is Pydantic?

Pydantic is a Python library for data validation. You define the shape of your data as a class, and Pydantic automatically checks that incoming data matches that shape — right types, required fields present, nothing unexpected sneaking through.

In a FastAPI application, Pydantic schemas serve two roles:

> ### Validating input
> When a `POST` or `PUT` request comes in, FastAPI uses the schema to validate the request body before your function even runs. If a required field is missing or a value is the wrong type, FastAPI rejects the request and returns a `422 Unprocessable Entity` error automatically — you don't have to write that check yourself.

> ### Shaping output
> When your route handler returns data, FastAPI uses the `response_model` schema to control exactly what gets serialized to JSON. Fields that aren't in the schema are stripped out. This means you can safely return a full database object from your handler without accidentally exposing columns you didn't intend to.

This separation between "what the database stores" and "what the API exposes" is intentional and important. In this project, for example, the `id` field is included in `CryptidResponse` (so clients can see which record they're working with) but excluded from `CryptidCreate` and `CryptidUpdate` (because the client has no business telling the database what ID to assign).

## What are those `@router` decorators?

The `@` syntax you see above each route handler function is a Python **decorator**. A decorator is a way of wrapping a function with additional behavior without changing the function itself. In this case, `@router.get("/")` is telling FastAPI: "when an HTTP GET request comes in for this URL, call this function."

```python
@router.get("/{cryptid_id}", response_model=CryptidResponse)
def read_cryptid(cryptid_id: int, db: Session = Depends(get_db)):
    ...
```

Breaking that down:

<div align="center">

| Part | What it means |
|---|---|
| `@router.get` | Register this function as a handler for GET requests |
| `"/{cryptid_id}"` | The URL pattern — `{cryptid_id}` is a path parameter that gets passed into the function |
| `response_model=CryptidResponse` | Use this Pydantic schema to shape and validate the response |
| `cryptid_id: int` | FastAPI sees the type hint and automatically converts the URL parameter to an integer |
| `db: Session = Depends(get_db)` | Dependency injection — FastAPI calls `get_db()` and passes the result in as `db` |

</div>

The router itself (`APIRouter`) is essentially a mini-app that groups related routes together. In `main.py`, `app.include_router(cryptids.router)` registers all of those routes with the main application at once, prefixed with `/cryptids`.

## Getting started

### Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Setup

Clone the repository and run the development server:

```bash
git clone https://github.com/yourusername/cryptid-api.git
cd cryptid-api
uv sync
uv run dev
```

`uv sync` installs all dependencies listed in `pyproject.toml` into a local `.venv`. `uv run dev` starts the server. The database is created and seeded with sample data automatically on first run.

### Accessing the API

Once running, the API is available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for the interactive documentation, where you can browse all endpoints and send test requests directly from your browser.

## Endpoints

All endpoints are under the `/cryptids` prefix.

<div align="center">

| Method | URL | Description |
|---|---|---|
| `GET` | `/cryptids/` | Return all cryptids (supports `skip` and `limit` query params) |
| `GET` | `/cryptids/{id}` | Return a single cryptid by ID |
| `POST` | `/cryptids/` | Create a new cryptid |
| `PUT` | `/cryptids/{id}` | Update an existing cryptid |
| `DELETE` | `/cryptids/{id}` | Delete a cryptid |

</div>

## Running the tests

The test suite uses `pytest` and runs against an in-memory SQLite database — meaning tests never touch the real database and always start from a clean state.

```bash
uv run pytest
```

> [!NOTE]
> The tests use FastAPI's dependency override system to swap out the real database session for a test one. This is the standard pattern for testing FastAPI applications without side effects.

## Database

This project uses **SQLite**, a file-based database that requires no server setup. The database file (`cryptids.db`) is created automatically in the project root when the server first starts. SQLite is a good choice for development and small projects — if you needed to scale this to a production environment, you would swap the connection string in `database.py` for PostgreSQL or another server-based database. The rest of the code would stay the same.