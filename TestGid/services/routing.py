from config import USE_GOOGLE, GOOGLE_API_KEY
from providers import google, osm

def build_map(start, end):
    """
    start, end = (lat, lon)
    """
    if USE_GOOGLE and GOOGLE_API_KEY:
        try:
            polyline = google.route(start, end, GOOGLE_API_KEY)
            return google.static_map(polyline, GOOGLE_API_KEY)
        except Exception:
            pass

    # fallback OSM
    coords = osm.route(start, end)
    return osm.static_map(coords)
