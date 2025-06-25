import pytest
from unittest.mock import patch, MagicMock
import project  # Make sure this matches your filename (project.py)

@pytest.fixture
def mock_geo_response():
    mock = MagicMock()
    mock.status_code = 200
    mock.json.return_value = [{
        "lat": 13.08,
        "lon": 80.27,
        "name": "Chennai"
    }]
    return mock

@pytest.fixture
def mock_weather_response():
    mock = MagicMock()
    mock.status_code = 200
    mock.json.return_value = {
        "main": {
            "temp": 300.15,
            "feels_like": 301.15,
            "temp_min": 298.15,
            "temp_max": 303.15,
            "humidity": 70,
            "pressure": 1013
        },
        "wind": {"speed": 5.5},
        "visibility": 10000,
        "weather": [{"main": "Rain"}]
    }
    return mock

@patch("project.requests.get")
def test_api_responses(mock_get, mock_geo_response, mock_weather_response):
    # Arrange mock responses in order of calls
    mock_get.side_effect = [mock_geo_response, mock_weather_response]

    # Simulate your API call flow (simplified version)
    city = "Chennai"
    api_key = "dummy"
    c1 = project.requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}")
    location_data = c1.json()[0]

    c2 = project.requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?lat={location_data['lat']}&lon={location_data['lon']}&appid={api_key}")
    weather_data = c2.json()

    # Assertions
    assert location_data['lat'] == 13.08
    assert weather_data['main']['temp'] == 300.15
    assert weather_data['weather'][0]['main'] == "Rain"
    assert weather_data['wind']['speed'] == 5.5
    
