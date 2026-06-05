import requests

def route(start, end):
    url = (
        "https://router.project-osrm.org/route/v1/foot/"
        f"{start[1]},{start[0]};{end[1]},{end[0]}"
    )
    r = requests.get(url, params={"overview": "full", "geometries": "geojson"}, timeout=5)
    r.raise_for_status()
    return r.json()["routes"][0]["geometry"]["coordinates"]

def static_map(coords):
    path = "|".join(f"{lat},{lon}" for lon, lat in coords)
    return f"https://staticmap.openstreetmap.de/staticmap.php?size=640x400&path={path}"
