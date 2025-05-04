import csv
import json
import os
from prospectgeo.config import current_config


def _get_base_dir(relative_path: str):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "..", "data", relative_path)


def load_json_file(relative_path: str):
    file_path = _get_base_dir(relative_path)
    with open(file_path, "r") as file:
        return json.load(file)


def load_csv_file_in_chunks(relative_path: str):
    file_path = _get_base_dir(relative_path)
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        chunk = []

        for row in reader:
            chunk.append(row)
            if len(chunk) >= current_config.read_chunk_size:
                yield chunk
                chunk = []

        if chunk:
            yield chunk
