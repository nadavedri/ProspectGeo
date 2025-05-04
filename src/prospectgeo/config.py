import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    postgres_user = os.getenv("POSTGRES_USER", "default_user")
    postgres_password = os.getenv("POSTGRES_PASSWORD", "default_password")
    postgres_db = os.getenv("POSTGRES_DB", "default_db")

    pipeline_name = os.getenv("PIPELINE_NAME", "prospect")
    read_chunk_size = int(os.getenv("READ_CHUNK_SIZE", 1000))
    write_chunk_size = int(os.getenv("WRITE_CHUNK_SIZE", 1000))
    max_retries = int(os.getenv("MAX_RETRIES", 3))
    retry_delay_min = int(os.getenv("RETRY_DELAY_MIN", 2))
    retry_delay_max = int(os.getenv("RETRY_DELAY_MAX", 10))


class DevelopmentConfig(Config):
    debug = True
    log_level = "DEBUG"


class ProductionConfig(Config):
    debug = False
    log_level = "INFO"


config_by_name = {"development": DevelopmentConfig, "production": ProductionConfig}

current_config = config_by_name.get(os.getenv("APP_ENV", "development"))
