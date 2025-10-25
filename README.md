# Product Catalog Microservice (TDD/BDD)

This project implements a simple product catalog microservice with a REST API using Flask and SQLAlchemy. It includes comprehensive pytest tests (>=95% coverage), linting with Ruff, and BDD scaffolding with Behave/Selenium.

## Stack
- Python 3.8+
- Flask, SQLAlchemy, Marshmallow
- pytest + pytest-cov
- Ruff (lint), Black (format)
- Behave, Selenium (Part 2 — UI scenarios)

## Run the service
```powershell
# 1) Create/activate a virtualenv (recommended)
# python -m venv .venv; .\.venv\Scripts\Activate.ps1

# 2) Install dependencies
pip install -r requirements.txt

# 3) Start the API
python run.py
```
Service runs at http://localhost:5000.

## API endpoints
- POST /products — Create a product
- GET /products/<id> — Read a product
- PUT /products/<id> — Update a product
- DELETE /products/<id> — Delete a product
- GET /products — List products, with filters:
  - category=A
  - available=true|false
  - name=substring (case-insensitive)

## Run tests (TDD)
```powershell
pytest
```
Coverage threshold is enforced at 95% (see `pytest.ini`).

## Lint
```powershell
ruff check .
```

## BDD (Part 2)
The `features/` folder contains 7 scenarios and step definitions that currently call the API directly so they can run without the provided UI. When you add the admin UI and Selenium setup, replace these steps with actual browser interactions. To run them against the API:

```powershell
# Start the API in another terminal first
python run.py

# Then run Behave (BASE_URL defaults to http://localhost:5000)
behave
```

If you have a different service URL, set `BASE_URL`:
```powershell
$env:BASE_URL = "http://127.0.0.1:5000"; behave
```

## Notes
- Database defaults to SQLite at `products.db` in the project folder. Tests use an in-memory SQLite DB.
- Adjust fields or filters as needed for your coursework, but ensure tests and coverage remain green.
