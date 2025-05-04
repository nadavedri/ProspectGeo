from prospectgeo.etl.extract import load_csv_file_in_chunks, load_json_file
from prospectgeo.etl.transform import transform_prospect_data
from prospectgeo.etl.load import batch_insert_data
from prospectgeo.utils.logging_config import logger
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from prospectgeo.config import current_config


@retry(
    stop=stop_after_attempt(current_config.max_retries),
    wait=wait_exponential(
        multiplier=1,
        min=current_config.retry_delay_min,
        max=current_config.retry_delay_max,
    ),
    retry=retry_if_exception_type(Exception),
)
def _run_prospect_pipeline():
    try:
        logger.info("Starting the 'prospect' ETL pipeline")
        country_regions = load_json_file("country-to-regions-mapping.json")
        logger.info("Loaded country-to-regions mapping")

        user_settings = load_json_file("users-locations-settings.json")
        logger.info("Loaded user location settings")

        for chunk_idx, chunk in enumerate(
            load_csv_file_in_chunks("prospects.csv"), start=1
        ):
            logger.info("Processing chunk %d", chunk_idx)
            transformed = transform_prospect_data(country_regions, user_settings, chunk)
            logger.info("Transformed chunk %d", chunk_idx)
            batch_insert_data(transformed)
            logger.info("Inserted chunk %d into the database", chunk_idx)

        logger.info("Successfully completed the 'prospect' ETL pipeline")
    except Exception as e:
        logger.error("Error occurred in the 'prospect' ETL pipeline: %s", e)
        raise


PIPELINES = {"prospect": _run_prospect_pipeline}


def run_etl_pipeline(name: str):
    logger.info("Starting ETL pipeline: '%s'", name)
    pipeline_fn = PIPELINES.get(name)
    if not pipeline_fn:
        logger.error(
            "Unknown pipeline '%s'. Available pipelines: %s",
            name,
            list(PIPELINES.keys()),
        )
        raise ValueError(
            f"Unknown pipeline '{name}'. Available: {list(PIPELINES.keys())}"
        )

    try:
        pipeline_fn()
        logger.info("ETL pipeline '%s' completed successfully", name)
    except Exception as e:
        logger.error("ETL pipeline '%s' failed: %s", name, e)
        raise
