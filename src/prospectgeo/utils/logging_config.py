import logging
import os
from dotenv import load_dotenv
# from prospectgeo.config import current_config

load_dotenv()

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(get_log_level())

    ch = logging.StreamHandler()
    ch.setLevel(get_log_level())

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger

def get_log_level():
    """Determine the log level based on the config """
    env_log_level = os.getenv("LOG_LEVEL", "DEBUG").upper()  
    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    return log_levels.get(env_log_level, logging.DEBUG)

logger = setup_logger()