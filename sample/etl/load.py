from typing import List, Dict
from .utils.db import ensure_table, upsert_rows

def load_dataframe(df) -> int:
    ensure_table()
    rows: List[Dict] = df.to_dict(orient="records")
    affected = upsert_rows(rows)
    return affected
