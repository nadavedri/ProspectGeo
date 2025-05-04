import pytest
from prospectgeo.etl.transform import transform_prospect_data


@pytest.fixture
def country_regions():
    return {
        "UA": ["Europe", "EMEA"],
        "US": ["North America"],
    }


@pytest.fixture
def user_settings():
    return {
        "user-1": {
            "location_include": ["Europe"],
            "location_exclude": None,
        },
        "user-2": {
            "location_include": ["US", "US-WA"],
            "location_exclude": ["US-TX"],
        },
    }


@pytest.fixture
def prospects_chunk():
    return [
        {
            "user_id": "user-1",
            "prospect_id": "1",
            "company_country": "UA",
            "company_state": "",
        },
        {
            "user_id": "user-2",
            "prospect_id": "2",
            "company_country": "US",
            "company_state": "WA",
        },
        {
            "user_id": "user-2",
            "prospect_id": "3",
            "company_country": "US",
            "company_state": "TX",
        },
        {
            "user_id": "user-3",  # Not in user_settings, should be skipped
            "prospect_id": "4",
            "company_country": "US",
            "company_state": "NE",
        },
    ]


def test_transform_prospect_data(country_regions, user_settings, prospects_chunk):
    results = transform_prospect_data(country_regions, user_settings, prospects_chunk)

    assert len(results) == 3

    assert results[0]["user_id"] == "user-1"
    assert results[0]["prospect_id"] == "1"
    assert results[0]["qualifies"] is True

    assert results[1]["user_id"] == "user-2"
    assert results[1]["prospect_id"] == "2"
    assert results[1]["qualifies"] is True

    assert results[2]["user_id"] == "user-2"
    assert results[2]["prospect_id"] == "3"
    assert results[2]["qualifies"] is False
