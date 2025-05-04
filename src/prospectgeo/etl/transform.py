from typing import Optional, Dict, List
from datetime import datetime, timezone
from prospectgeo.utils.logging_config import logger  # Import the logger


def _prospect_qualifies(
    company_country: str,
    company_state: Optional[str],
    user_settings: Dict[str, Optional[List[str]]],
    country_to_region: Dict[str, List[str]],
) -> bool:
    logger.debug(
        "Evaluating prospect qualification for country: %s, state: %s",
        company_country,
        company_state,
    )
    location_include = user_settings.get("location_include", [])
    location_exclude = user_settings.get("location_exclude") or []

    if company_country == "US" and company_state:
        location = f"US-{company_state}"
    else:
        location = company_country

    logger.debug("Derived location: %s", location)

    if location in location_include:
        if location in location_exclude:
            logger.debug(
                "Location %s is in both include and exclude lists. Excluding.", location
            )
            return False
        logger.debug("Location %s qualifies based on include list.", location)
        return True

    regions = country_to_region.get(company_country, [])
    logger.debug("Regions for country %s: %s", company_country, regions)
    for region in regions:
        if region in location_include:
            if location in location_exclude:
                logger.debug(
                    "Region %s qualifies, but location %s is excluded.",
                    region,
                    location,
                )
                return False
            logger.debug("Region %s qualifies.", region)
            return True

    logger.debug("Location %s does not qualify.", location)
    return False


def transform_prospect_data(country_regions, user_settings, prospects_chunk):
    logger.info(
        "Starting transformation of prospects chunk with %d records.",
        len(prospects_chunk),
    )
    qualification_results = []

    for prospect in prospects_chunk:
        user_id = prospect["user_id"]
        logger.debug("Processing prospect with user_id: %s", user_id)
        settings = user_settings.get(user_id)
        if not settings:
            logger.warning(
                "No settings found for user_id: %s. Skipping prospect.", user_id
            )
            continue  # or handle default

        qualifies = _prospect_qualifies(
            company_country=prospect["company_country"],
            company_state=prospect.get("company_state"),
            user_settings=settings,
            country_to_region=country_regions,
        )
        result = {
            "user_id": user_id,
            "prospect_id": prospect["prospect_id"],
            "qualifies": qualifies,
            "qualification_timestamp": datetime.now(timezone.utc),
        }
        logger.debug(
            "Processed prospect_id: %s for user_id: %s. Qualification result: %s",
            prospect["prospect_id"],
            user_id,
            qualifies,
        )
        qualification_results.append(result)

    logger.info(
        "Completed transformation of prospects chunk. Total qualified: %d",
        len(qualification_results),
    )
    return qualification_results
