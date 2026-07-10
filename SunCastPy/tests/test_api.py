from fastapi.testclient import TestClient

from SunCastPy.api import app

client = TestClient(app)


def test_get_city_forecast(monkeypatch):
    """Verify the forecast endpoint returns the expected JSON."""

    response = client.get("/forecast_city/Mayaguez")

    assert response.status_code == 200
    assert response.json() is not None
