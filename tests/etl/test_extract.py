import csv
import os
from prospectgeo.etl.extract import load_json_file, load_csv_file_in_chunks


def test_load_json_file(tmp_path):
    test_data = {"key": "value"}
    test_file = tmp_path / "test.json"
    test_file.write_text('{"key": "value"}')

    data = load_json_file(str(test_file))
    assert data == test_data


def test_load_csv_file_in_chunks_env(tmp_path):
    csv_path = tmp_path / "prospects.csv"
    headers = ["user_id", "prospect_id", "company_country", "company_state"]
    rows = [
        ["u1", "1", "US", "CA"],
        ["u2", "2", "US", "WA"],
        ["u3", "3", "UA", ""],
        ["u4", "4", "US", "TX"],
    ]

    with csv_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    chunks = list(load_csv_file_in_chunks(csv_path))

    assert len(chunks) == 1
    assert chunks[0][0]["user_id"] == "u1"
    assert chunks[0][1]["company_state"] == "WA"
