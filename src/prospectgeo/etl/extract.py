import csv
import json
import os
from prospectgeo.config import current_config
from prospectgeo.utils.logging_config import logger

def _get_base_dir(relative_path: str):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logger.debug("Base directory resolved to: %s", base_dir)
    return os.path.join(base_dir, "..", "data", relative_path)


def load_json_file(relative_path: str):
    file_path = _get_base_dir(relative_path)
    logger.info("Loading JSON file from: %s", file_path)
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            logger.info("Successfully loaded JSON file with %d keys", len(data))
            return data
    except Exception as e:
        logger.error("Failed to load JSON file: %s", e)
        raise


def load_csv_file_in_chunks(relative_path: str):
    file_path = _get_base_dir(relative_path)
    logger.info("Loading CSV file in chunks from: %s", file_path)
    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            chunk = []
            row_count = 0

            for row in reader:
                chunk.append(row)
                row_count += 1
                if len(chunk) >= current_config.read_chunk_size:
                    logger.info("Yielding chunk of size %d after processing %d rows", len(chunk), row_count)
                    yield chunk
                    chunk = []

            if chunk:
                logger.info("Yielding final chunk of size %d after processing %d rows", len(chunk), row_count)
                yield chunk
    except Exception as e:
        logger.error("Failed to load CSV file in chunks: %s", e)
        raise
