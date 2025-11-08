import pandas as pd
from typing import List, Dict

COLUMNS = {
    "id": "source_id",
    "name": "name",
    "brewery_type": "type",
    "city": "city",
    "state": "state",
    "country": "country",
    "postal_code": "postal_code",
    "website_url": "website",
    "latitude": "lat",
    "longitude": "lon",
}

def normalize_records(rows: List[Dict]) -> pd.DataFrame:
    df = pd.json_normalize(rows)

    # Select and rename
    keep = [c for c in COLUMNS.keys() if c in df.columns]
    df = df[keep].rename(columns=COLUMNS)

    # Types
    df["name"] = df["name"].astype(str).str.strip()
    df["type"] = df["type"].astype("category")
    if "lat" in df.columns:
        df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    if "lon" in df.columns:
        df["lon"] = pd.to_numeric(df["lon"], errors="coerce")

    # Deduplicate on source_id
    if "source_id" in df.columns:
        df = df.drop_duplicates(subset=["source_id"]) 

    # Add load_ts
    df["load_ts"] = pd.Timestamp.utcnow()

    return df
