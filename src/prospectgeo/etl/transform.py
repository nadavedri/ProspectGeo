from typing import Optional, Dict, List
from datetime import datetime

def _qualifies(
    company_country: str,
    company_state: Optional[str],
    user_settings: Dict[str, Optional[List[str]]],
    country_to_region: Dict[str, List[str]]
) -> bool:

    location_include = user_settings.get("location_include", [])
    location_exclude = user_settings.get("location_exclude") or []

    if company_country == "US" and company_state:
        location = f"US-{company_state}"
    else:
        location = company_country

    if location in location_include:
        if location in location_exclude:
            return False
        return True

    regions = country_to_region.get(company_country, [])
    for region in regions:
        if region in location_include:
            if location in location_exclude:
                return False
            return True

    return False

def transform_data(country_regions, user_settings, prospects_chunk):
    qualification_results = []

    for user_id, settings in user_settings.items():
        for prospect in prospects_chunk:
            result = {
                'user_id': user_id,
                'prospect_id': prospect['prospect_id'],
                'qualifies': _qualifies(
                    company_country=prospect['company_country'],
                    company_state=prospect.get('company_state'),
                    user_settings=settings,
                    country_to_region=country_regions
                ),
                'qualification_timestamp': datetime.utcnow()
            }
            qualification_results.append(result)

    return qualification_results