import requests

def route(start, end, api_key):
    r = requests.get(
        "https://maps.googleapis.com/maps/api/directions/json",
        params={
            "origin": f"{start[0]},{start[1]}",
            "destination": f"{end[0]},{end[1]}",
            "mode": "walking",
            "key": api_key
        },
        timeout=5
    )
    r.raise_for_status()
    return r.json()["routes"][0]["overview_polyline"]["points"]

def static_map(polyline, api_key):
    return (
        "https://maps.googleapis.com/maps/api/staticmap"
        f"?size=640x400&path=enc:{polyline}&key={api_key}"
    )
