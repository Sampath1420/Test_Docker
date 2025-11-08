import pandas as pd
from etl.transform import normalize_records

def test_normalize_records_basic():
    rows = [
        {
            "id": "abc123",
            "name": "Foo Brewery ",
            "brewery_type": "micro",
            "city": "Austin",
            "state": "Texas",
            "country": "United States",
            "postal_code": "78701",
            "website_url": "http://example.com",
            "latitude": "30.1",
            "longitude": "-97.7",
        },
        {
            "id": "abc123",  # duplicate
            "name": "Foo Brewery",
            "brewery_type": "micro",
        },
    ]

    df = normalize_records(rows)
    assert "source_id" in df.columns
    assert df.shape[0] == 1  # dedup
    assert df.loc[df.index[0], "name"] == "Foo Brewery"
    assert pd.api.types.is_datetime64_any_dtype(df["load_ts"]) 
