import logging

import pytest
from fastapi.testclient import TestClient

from SunCastPy.api import app

logger = logging.getLogger(__name__)
client = TestClient(app)
DEFAULTS = {
    "city": "San Juan",
    "flatten": True,
    "limit": 1,
}


class Test_City_Forecast:
    @pytest.mark.parametrize(
        ("overrides"),
        (
            pytest.param({}, id="default"),
            pytest.param({"flatten": False}, id="flatten_false"),
            pytest.param({"limit": 3}, id="limit_3"),
        ),
    )
    def test_get_city_forecast(
        self, mock_get_request, overrides, request, expected_data_group_by_dayname
    ):
        """Verify the forecast endpoint returns the expected JSON."""
        params = {**DEFAULTS, **overrides}
        logger.info("Test values:")
        for key, val in params.items():
            logger.info(f"{key} = {val}")
        html_city = params["city"].replace(" ", "%20")

        # Only add the extra url parameters if its not using default values
        current_id = request.node.callspec.id
        if current_id == "default":
            response = client.get(f"/forecast_city/{html_city}")
        else:
            response = client.get(
                f"/forecast_city/{html_city}?flatten={params['flatten']}&limit={params['limit']}"
            )

        # The count of forecast values changes if its flattened or not
        if params["flatten"]:
            count = expected_data_group_by_dayname["Sunday 2026-03-22"]["flattened"]
        else:
            count = expected_data_group_by_dayname["Sunday 2026-03-22"]["default"]

        # Run the command and verify outputs
        response_data = response.json()
        assert response.status_code == 200
        assert response_data is not None
        assert len(response_data.keys()) == params["limit"]
        assert len(response_data["Sunday 2026-03-22"]) == count

    def test_invalid_input(self):
        response = client.get(
            f"/forecast_city/{DEFAULTS['city']}?flatten={DEFAULTS['flatten']}&limit=10"
        )

        assert response.status_code == 404

        assert response.json() == {
            "detail": "Invalid number of days to limit the forecast."
        }
