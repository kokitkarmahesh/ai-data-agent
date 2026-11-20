
from pathlib import Path
import duckdb

# Project root folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Location of our DuckDB database
DATABASE_PATH = PROJECT_ROOT / "data" / "banking.duckdb"


def get_connection(read_only=False):
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    return duckdb.connect(
        str(DATABASE_PATH),
        read_only=read_only
    )
