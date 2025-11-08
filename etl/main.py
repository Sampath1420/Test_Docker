from etl.extract import fetch_raw_json
from etl.transform import normalize_records
from etl.load import load_dataframe

def run():
    raw = fetch_raw_json()
    df = normalize_records(raw)
    n = load_dataframe(df)
    print(f"Loaded/updated rows: {n}")

if __name__ == "__main__":
    run()
