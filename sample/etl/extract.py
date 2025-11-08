from typing import List
import requests

from .config import settings

def fetch_raw_json() -> List[dict]:
    url = settings.source_url
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if not isinstance(data, list):
        raise ValueError("Expected list JSON from source API")
    return data
