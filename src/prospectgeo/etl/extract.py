import csv
import json
from prospectgeo.config import current_config


def load_json_file(path):
    with open(path, 'r') as file:
        return json.load(file)

def load_csv_file_in_chunks(path):
    with open(path, 'r') as file:
        reader = csv.DictReader(file)
        chunk = []
        
        for row in reader:
            chunk.append(row)
            if len(chunk) >= current_config.read_chunk_size:
                yield chunk
                chunk = []
        
        if chunk:
            yield chunk