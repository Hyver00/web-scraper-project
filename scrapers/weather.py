import requests
from database.db_manager import insert_weather

# Open-Meteo — free weather API, no API key required
GEO_URL     = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

CITIES = ["Bucaramanga", "Bogota", "Medellin", "Cali", "Cartagena"]


def get_coordinates(city: str):
    """Resolve a city name to latitude/longitude using Open-Meteo Geocoding."""
    try:
        resp = requests.get(GEO_URL, params={"name": city, "count": 1}, timeout=10)
        resp.raise_for_status()
        results = resp.json().get("results")
        if not results:
            print(f"⚠️  City not found: {city}")
            return None
        result = results[0]
        return result["latitude"], result["longitude"], result.get("country_code", "")
    except requests.RequestException as e:
        print(f"❌ Geocoding error for {city}: {e}")
        return None


def wmo_description(code: int) -> str:
    """Convert a WMO weather interpretation code to a human-readable string."""
    descriptions = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Icy fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
        80: "Slight showers", 81: "Moderate showers", 82: "Violent showers",
        95: "Thunderstorm", 96: "Thunderstorm with hail"
    }
    return descriptions.get(code, f"WMO code {code}")


def scrape_weather():
    """Fetch current weather for each city and store it in the database."""
    print("🔄 Fetching weather data...")
    saved = 0

    for city in CITIES:
        coords = get_coordinates(city)
        if not coords:
            continue

        lat, lon, country = coords
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "hourly": "relativehumidity_2m,apparent_temperature,windspeed_10m",
            "forecast_days": 1,
            "timezone": "auto"
        }

        try:
            resp = requests.get(WEATHER_URL, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            current = data.get("current_weather", {})
            hourly  = data.get("hourly", {})

            # Pick the first hourly value as current-hour approximation
            humidity    = hourly.get("relativehumidity_2m", [None])[0]
            feels_like  = hourly.get("apparent_temperature", [None])[0]
            wind        = hourly.get("windspeed_10m", [None])[0]
            description = wmo_description(current.get("weathercode", 0))

            insert_weather(
                city=city,
                country=country,
                temperature=current.get("temperature"),
                feels_like=feels_like,
                humidity=humidity,
                description=description,
                wind_kmh=wind
            )
            saved += 1

        except requests.RequestException as e:
            print(f"❌ Weather error for {city}: {e}")

    print(f"✅ Weather data saved for {saved} cities.")


if __name__ == "__main__":
    scrape_weather()