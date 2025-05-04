from prospectgeo.etl.extract import load_csv_file_in_chunks, load_json_file
from prospectgeo.etl.transform import transform_prospect_data
from prospectgeo.etl.load import batch_insert_data


def _run_prospect_pipeline():
    country_regions = load_json_file("country-to-regions-mapping.json")
    user_settings = load_json_file("users-locations-settings.json")

    for chunk in load_csv_file_in_chunks("prospects.csv"):
        transformed = transform_prospect_data(country_regions, user_settings, chunk)
        batch_insert_data(transformed)


PIPELINES = {"prospect": _run_prospect_pipeline}


def run_etl_pipeline(name: str):
    pipeline_fn = PIPELINES.get(name)
    if not pipeline_fn:
        raise ValueError(
            f"Unknown pipeline '{name}'. Available: {list(PIPELINES.keys())}"
        )

    print(f"Running '{name}' ETL pipeline")
    pipeline_fn()
