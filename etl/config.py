from dataclasses import dataclass
import os

@dataclass
class Settings:
    source_url: str = os.getenv("SOURCE_URL", "https://api.openbrewerydb.org/v1/breweries?per_page=200")
    pg_db: str = os.getenv("POSTGRES_DB", "sp")
    pg_user: str = os.getenv("POSTGRES_USER", "postgres")
    pg_password: str = os.getenv("POSTGRES_PASSWORD", "#Sampath123")
    pg_host: str = os.getenv("POSTGRES_HOST", "db")
    pg_port: int = int(os.getenv("POSTGRES_PORT", 5432))

    @property
    def pg_dsn(self) -> str:
        return (
            f"dbname={self.pg_db} user={self.pg_user} password={self.pg_password} "
            f"host={self.pg_host} port={self.pg_port}"
        )

settings = Settings()
