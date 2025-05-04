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

class DevelopmentConfig(Config):
    debug = True

class ProductionConfig(Config):
        debug = False

config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}

current_config = config_by_name.get(os.getenv("APP_ENV", "development"))