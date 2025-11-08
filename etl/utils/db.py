import psycopg
from psycopg.rows import dict_row
from contextlib import contextmanager
from ..config import settings

@contextmanager
def conn_cursor():
    with psycopg.connect(settings.pg_dsn) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            yield conn, cur

def ensure_table():
    sql = """
    CREATE TABLE IF NOT EXISTS public.breweries (
        source_id text PRIMARY KEY,
        name text NOT NULL,
        type text,
        city text,
        state text,
        country text,
        postal_code text,
        website text,
        lat double precision,
        lon double precision,
        load_ts timestamptz NOT NULL
    );
    """
    with conn_cursor() as (conn, cur):
        cur.execute(sql)
        conn.commit()

def upsert_rows(rows):
    if not rows:
        return 0

    cols = [
        "source_id", "name", "type", "city", "state", "country",
        "postal_code", "website", "lat", "lon", "load_ts"
    ]

    placeholders = ",".join(["%s"] * len(cols))
    insert_sql = f"""
        INSERT INTO public.breweries ({','.join(cols)})
        VALUES ({placeholders})
        ON CONFLICT (source_id) DO UPDATE SET
            name = EXCLUDED.name,
            type = EXCLUDED.type,
            city = EXCLUDED.city,
            state = EXCLUDED.state,
            country = EXCLUDED.country,
            postal_code = EXCLUDED.postal_code,
            website = EXCLUDED.website,
            lat = EXCLUDED.lat,
            lon = EXCLUDED.lon,
            load_ts = EXCLUDED.load_ts;
    """

    data = [tuple(row.get(c) for c in cols) for row in rows]

    with conn_cursor() as (conn, cur):
        cur.executemany(insert_sql, data)
        conn.commit()
        return cur.rowcount
