---
description: Automated Testing Workflow for the FastAPI Fusion Application
---

# FastAPI Application Testing Workflow

This workflow describes how to run automated tests for the FastAPI Fusion application using `pytest` and `httpx`.

## Prerequisites
Ensure that all testing dependencies are installed.

// turbo
```bash
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Running the Unit Tests

Execute the test suite using `pytest`. The `pytest.ini` file is configured to run all tests inside the `tests/` directory with `pytest-asyncio` enabled.

// turbo
```bash
source .venv/bin/activate
pytest tests/ -v
```

## E2E Database Considerations

If your tests require active databases (PostgreSQL, MySQL, MongoDB):
1. Ensure the development databases are running, or mock the database dependencies using FastAPI's `app.dependency_overrides`.
2. Avoid running destructive tests (like wiping out `TblUser`) against the primary `.env.development` database. Use a separate test database instead.

## Adding New Tests

When adding new features:
1. Create a `test_*.py` file inside the `tests/` directory.
2. Initialize an async testing client (`httpx.AsyncClient`) tied to `app`.
3. Verify endpoint response codes and payloads.
