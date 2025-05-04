from .client import get_db_client
from .schemas.postgres.qualification_results_schema import (
    create_qualification_results_schema,
)


def create_all_schemas():
    postgres_conn = get_db_client("postgres")
    create_qualification_results_schema(postgres_conn)
