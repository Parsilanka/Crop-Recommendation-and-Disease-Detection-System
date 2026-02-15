import json
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    import urllib.request
    HAS_REQUESTS = False

def get_weather(lat=None, lon=None): 
    # Default to Nairobi if no coordinates provided
    if not lat or not lon:
        lat = -1.2921
        lon = 36.8219
        
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    
    try:
        if HAS_REQUESTS:
            response = requests.get(url)
            data = response.json()
        else:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
        
        current = data.get('current_weather', {})
        
        # Get location name
        location_name = "Unknown Location"
        try:
            # Use BigDataCloud free reverse geocoding (no API key needed for client-side, but let's try server-side)
            # Or Open-Meteo Geocoding API (search) doesn't do reverse.
            # Let's use a simple public API or just return coordinates if fails.
            # Nominatim is good but requires User-Agent.
            
            geo_url = f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={lat}&longitude={lon}&localityLanguage=en"
            
            if HAS_REQUESTS:
                geo_res = requests.get(geo_url)
                geo_data = geo_res.json()
            else:
                with urllib.request.urlopen(geo_url) as r:
                    geo_data = json.loads(r.read().decode())
            
            # Build location text
            # BigDataCloud returns: city, locality, principalSubdivision, countryName
            
            city = geo_data.get('city', '')
            locality = geo_data.get('locality', '')
            principal = geo_data.get('principalSubdivision', '')
            country = geo_data.get('countryName', '')
            
            # Prioritize specific name: Locality > City > Principal Subdivision
            if locality:
                location_name = locality
            elif city:
                location_name = city
            elif principal:
                location_name = principal
            else:
                location_name = "Unknown Location"
                
            # Append Country if not empty and not redundant (optional, maybe user just wants city)
            # User request: "if meru displays meru". So maybe just the city name is better?
            # Let's keep it simple: "City, Country" or just "City" if country is Kenya (implied context)
            
            if country and country != location_name and country != "Kenya":
                 location_name = f"{location_name}, {country}"
                 
            if not location_name.strip(): location_name = "Unknown Location"
            
        except Exception as e:
            print(f"Reverse geocode failed: {e}")
            location_name = f"Lat: {lat}, Lon: {lon}"

        return {
            'temperature': current.get('temperature'),
            'windspeed': current.get('windspeed'),
            'weathercode': current.get('weathercode'),
            'is_day': current.get('is_day'),
            'location': location_name
        }
    except Exception as e:
        print(f"Weather fetch failed: {e}")
        return None

def get_weather_desc(code):
    # Simplified WMO codes
    if code == 0: return "Clear sky"
    if code in [1, 2, 3]: return "Partly cloudy"
    if code in [45, 48]: return "Fog"
    if code in [51, 53, 55]: return "Drizzle"
    if code in [61, 63, 65]: return "Rain"
    if code in [80, 81, 82]: return "Showers"
    if code in [95, 96, 99]: return "Thunderstorm"
    return "Unknown"
