import json
import requests


def get_weather(city: str) -> dict:
    """Fetch current weather data for the given city from wttr.in."""
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def print_weather(data: dict, city: str) -> None:
    """Print a simple weather summary from wttr.in JSON data."""
    current = data.get("current_condition", [{}])[0]
    nearest_area = data.get("nearest_area", [{}])[0]
    area_name = nearest_area.get("areaName", [{}])[0].get("value", city)
    region = nearest_area.get("region", [{}])[0].get("value", "Unknown")
    country = nearest_area.get("country", [{}])[0].get("value", "Unknown")

    temp_c = current.get("temp_C", "N/A")
    feels_like_c = current.get("FeelsLikeC", "N/A")
    weather_desc = current.get("weatherDesc", [{}])[0].get("value", "N/A")
    humidity = current.get("humidity", "N/A")
    wind_kph = current.get("windspeedKmph", "N/A")
    precipitation_mm = current.get("precipMM", "N/A")

    print(f"\nWeather for: {area_name}, {region}, {country}")
    print("--------------------------------------")
    print(f"Condition: {weather_desc}")
    print(f"Temperature: {temp_c}°C")
    print(f"Feels like: {feels_like_c}°C")
    print(f"Humidity: {humidity}%")
    print(f"Wind speed: {wind_kph} km/h")
    print(f"Precipitation: {precipitation_mm} mm")
    print("--------------------------------------")

    today = data.get("weather", [{}])[0]
    if today:
        max_temp = today.get("maxtempC", "N/A")
        min_temp = today.get("mintempC", "N/A")
        avg_temp = today.get("avgtempC", "N/A")
        print(f"Today: High {max_temp}°C, Low {min_temp}°C, Avg {avg_temp}°C")


def main() -> None:
    print("Simple Weather App using requests and JSON By Sarfaraz Sayyad")
    city = input("Enter a city name: ").strip()
    if not city:
        print("Please enter a valid city name.")
        return

    try:
        data = get_weather(city)
        print_weather(data, city)
    except requests.HTTPError as exc:
        print(f"HTTP error while contacting weather service: {exc}")
    except requests.RequestException as exc:
        print(f"Network error: {exc}")
    except json.JSONDecodeError:
        print("Could not decode weather service response as JSON.")
    except Exception as exc:
        print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    main()
