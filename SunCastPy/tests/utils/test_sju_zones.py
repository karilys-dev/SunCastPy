# pylint: disable=redefined-outer-name
import pytest

from SunCastPy.data.sju_zones import get_all_zones, group_zones
from SunCastPy.data.zones_url import SJU_ZONES

expected = {
    "Central Interior": "Aibonito",
    "Culebra": "Culebra",
    "Eastern Interior": "Aguas Buenas",
    "Mayaguez and Vicinity": "Aguada",
    "North Central": "Arecibo",
    "Northeast": "Canovanas",
    "Northwest": "Aguadilla",
    "Ponce and Vicinity": "Guayanilla",
    "San Juan and Vicinity": "Bayamon",
    "Southeast": "Arroyo",
    "Southwest": "Cabo Rojo",
    "Vieques": "Vieques",
    "Western Interior": "Adjuntas",
}


@pytest.fixture(scope="module")
def data_group_zones() -> dict:
    return group_zones(SJU_ZONES)


def test_group_zones(data_group_zones):
    assert len(data_group_zones) < len(SJU_ZONES)
    assert list(data_group_zones.keys()) == list(expected.keys())


@pytest.mark.parametrize(
    ("attribute"),
    ["cities", "url", "location"],
)
def test_group_zone_attributes(attribute, data_group_zones):
    assert attribute in list(list(data_group_zones.values())[0].keys())


@pytest.mark.parametrize(
    ("zone"),
    list(expected.keys()),
)
def test_zone_has_city(zone, data_group_zones):
    assert expected[zone] in data_group_zones[zone]["cities"]


def test_get_all_zones(mock_city, mock_city_url, sju_data):
    result = get_all_zones()
    assert "Test" in result
    assert result["Test"]["url"] == sju_data["properties"]["forecastHourly"]
    assert result["Test"]["forecastZone"] == sju_data["properties"]["forecastZone"]
