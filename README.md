# TaskBoard

## Purpose
TaskBoard is a small task-management REST API (FastAPI) used as the running example of the ESIEE DevSecOps course. Version 0.1 exposes CRUD endpoints on tasks with strict input validation and automated tests.

## Requirements
- Python 3.11 or newer
- Git

## Installation
```bash
git clone <repo-url> taskboard
cd taskboard
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
uvicorn app.main:app --reload
```
Then open http://127.0.0.1:8000/docs (Swagger UI).

| Method | Path | Description | Success |
| --- | --- | --- | --- |
| GET | `/health` | Health check | 200 |
| POST | `/tasks` | Create a task | 201 |
| GET | `/tasks` | List tasks | 200 |
| GET | `/tasks/{task_id}` | Get one task | 200 |
| PATCH | `/tasks/{task_id}` | Update only the fields sent | 200 |
| DELETE | `/tasks/{task_id}` | Delete a task | 204 |

## Tests
```bash
pytest -v
```

## Environment variables
Copy `.env.example` to `.env` and adjust the values locally. **Never commit `.env`** (it is ignored by `.gitignore`).

| Variable | Purpose |
| --- | --- |
| `APP_ENV` | Environment name (`development`, …) |
| `LOG_LEVEL` | Log verbosity |
| `DATABASE_URL` | Database connection string (used in a later session) |
| `SECRET_KEY` | Application secret (used in a later session) |

## Project structure
```
taskboard/
├── app/
│   ├── main.py          # FastAPI app and /health
│   ├── schemas.py       # Pydantic models and validation rules
│   └── routers/
│       └── tasks.py     # /tasks CRUD endpoints (in-memory store)
├── tests/
│   ├── conftest.py      # Fixtures: test client, clean store
│   └── test_tasks.py    # API tests
├── docs/
│   └── security-notes.md
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```


## Input validation

Invalid input returns HTTP 422. A valid positive task ID that does not
exist returns HTTP 404.

| Field | Validation rule |
| --- | --- |
| title | Required on creation, trimmed, 1–200 characters, never null |
| description | Optional and nullable, maximum 2,000 characters |
| status | todo, in_progress or done; defaults to todo; never null |
| Unknown fields | Rejected, including id and owner |
| task_id | Positive integer |

PATCH updates only the supplied fields. Omitted fields keep their current
values. Sending description: null clears the description.
Sending title: null or status: null is rejected.
## Storage
Tasks are stored in memory only. All data is lost when the server restarts. A database will replace it in a later session.
