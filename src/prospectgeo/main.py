from prospectgeo.db import setup_databases
from prospectgeo.etl.manager import run_etl_pipeline
from prospectgeo.config import current_config


def main():
    setup_databases()
    run_etl_pipeline(current_config.pipeline_name)
