# Dockerized ETL/ELT Pipeline (Postgres + GitHub Actions)

This repository contains a complete ETL/ELT example that runs entirely in Docker and is executed by a GitHub Actions pipeline on every push.

## Quick start (local)
1. Copy env file:
   ```bash
   cp .env.example .env
   ```
2. Start the stack:
   ```bash
   docker compose up --build
   ```
   The ETL container will run once and exit after loading data. Postgres and pgAdmin remain available.

3. Explore the DB:
   - pgAdmin at <http://localhost:5050> (use credentials from `.env`).
   - Register a new server in pgAdmin with:
     - Host: `db`
     - Port: `5432`
     - Database: `brewdata`
     - Username: `brewuser`
     - Password: `brewpass`

4. Re-run the ETL manually:
   ```bash
   docker compose run --rm etl
   ```

## Switching sources
Edit `SOURCE_URL` in `.env` to another API or CSV endpoint that returns a list-like JSON. Update `etl/transform.py` to map fields to your target schema.

## ELT mode
If you prefer ELT, load raw JSON to a `raw.breweries` table first and use SQL (dbt, SQL files, or views) to transform. You can adapt `etl/load.py` to insert raw JSON and create a separate `sql/` folder for transformations.

## CI with GitHub Actions
- The workflow in `.github/workflows/ci.yml` runs unit tests, spins up Postgres, and executes the ETL in Docker.
- On success, the job prints a count of rows loaded.

## Extending
- Add scheduling with cron (GitHub Actions `schedule`) or run in Airflow.
- Add alerts on load failures.
- Add data quality checks in `tests/`.

## Troubleshooting
- If pgAdmin can’t connect, ensure the server name points to host `db` (Docker network).
- If the API rate limits, reduce `per_page` or add retries/backoff in `etl/extract.py`.
