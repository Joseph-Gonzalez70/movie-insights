import json
from urllib.parse import  urlunparse, urlencode
from six import string_types

def build_url(path, scheme, netloc, params):
    """Build a URL from a path, scheme, netloc, and query parameters."""
    query = urlencode({k:v if isinstance(v, string_types) else json.dumps(v) for k,v in params.items()})
    url = urlunparse((scheme, netloc, path, '', query, ''))   
    return url