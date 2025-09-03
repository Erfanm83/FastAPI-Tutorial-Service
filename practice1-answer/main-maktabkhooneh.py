"""
FastAPI wrapper for course provider APIs
========================================

This module exposes a small set of endpoints that act as a gateway to
course provider APIs.  The primary purpose of this service is to
document the upstream routes and provide a unified entry point for
retrieving course categories and course listings from different
providers.  Initially only the ``maktabkhooneh`` provider is
implemented, but additional providers can easily be added by updating
the ``PROVIDERS`` dictionary.

The API exposes three read‑only endpoints per provider:

* ``/providers/{provider}/categories`` – returns the provider's
  top‑level categories as delivered by the upstream API.
* ``/providers/{provider}/categories/{slug}`` – returns metadata about
  a specific category (e.g. title, description, child categories).
* ``/providers/{provider}/categories/{slug}/search`` – returns a paged
  list of courses within the specified category.  Any query
  parameters are forwarded to the upstream API to control paging or
  sorting.

This gateway does **not** persist any data and does not modify the
responses returned by upstream providers.  It merely proxies the
requests and relays the JSON responses.  Since the service only
supports GET operations, it can be safely used as a read‑only API.

If you wish to add new providers, add a new entry to the
``PROVIDERS`` dictionary with at least a ``base_url`` pointing to
the provider's categories endpoint.  See the existing ``maktabkhooneh``
entry for reference.
"""

from typing import Any, Dict

import requests
from fastapi import Depends, FastAPI, HTTPException, Path, Query, Request
from fastapi.responses import JSONResponse


def get_http_client() -> requests.Session:
    """Return a ``requests`` session with sensible defaults.

    Using a session allows HTTP keep‑alive and makes it easier to
    override headers for all outbound requests.  If you need to
    customise the client (e.g. set timeouts or proxies), adjust
    this function accordingly.
    """
    session = requests.Session()
    # Set a default user agent so the upstream provider doesn’t
    # silently block the request.  Some services return 403 for
    # unknown user agents.
    session.headers.update(
        {
            "User-Agent": "CourseProviderGateway/1.0 (+https://example.com)",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
        }
    )
    return session


app = FastAPI(
    title="Course Providers Gateway API",
    version="1.0.0",
    description=(
        "A simple read‑only API that proxies selected routes from course providers.\n"
        "Initially supports the maktabkhooneh provider, but additional providers\n"
        "can be configured by updating the PROVIDERS mapping."
    ),
)

# Mapping of provider identifiers to configuration
# Each provider entry must define at least a ``base_url`` that
# resolves to the upstream categories endpoint.  Additional keys may
# be defined in future (e.g. API keys, headers).
PROVIDERS: Dict[str, Dict[str, Any]] = {
    "maktabkhooneh": {
        "base_url": "https://maktabkhooneh.org/api/v1/courses/categories",
    },
}


def get_provider_config(provider: str) -> Dict[str, Any]:
    """Return the configuration for a given provider.

    Raises:
        HTTPException: if the provider is not supported.
    """
    config = PROVIDERS.get(provider)
    if not config:
        raise HTTPException(status_code=404, detail=f"Unknown provider '{provider}'")
    return config


def proxy_request(
    url: str, session: requests.Session, params: Dict[str, Any] | None = None
) -> JSONResponse:
    """Proxy a GET request to an upstream URL and return the JSON response.

    Args:
        url: The full URL to call on the upstream provider.
        session: An HTTP session with defaults applied.
        params: Optional query parameters to include with the request.

    Returns:
        A ``JSONResponse`` containing the upstream JSON body and status code.

    Raises:
        HTTPException: if the upstream returns a non‑JSON response or
        non‑200 status code.
    """
    try:
        response = session.get(url, params=params, timeout=30)
    except requests.RequestException as exc:
        # Network failures, timeouts, DNS errors etc.
        raise HTTPException(
            status_code=502,
            detail=f"Failed to reach upstream provider: {exc}",
        )
    # Propagate HTTP status codes >= 400 to the client
    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Upstream responded with status {response.status_code}",
        )
    # Ensure the upstream returned JSON; this will raise if invalid
    try:
        data = response.json()
    except ValueError:
        raise HTTPException(
            status_code=502,
            detail="Upstream returned invalid JSON",
        )
    return JSONResponse(content=data, status_code=response.status_code)


@app.get("/providers/{provider}/categories", tags=["Categories"])
def list_categories(
    provider: str = Path(..., description="The provider name, e.g. 'maktabkhooneh'"),
    session: requests.Session = Depends(get_http_client),
) -> JSONResponse:
    """Retrieve the full categories list from the specified provider.

    This endpoint proxies the provider's ``/categories`` route and returns
    exactly the JSON provided by the upstream service.  See the provider
    documentation for the response schema.
    """
    config = get_provider_config(provider)
    url = config["base_url"]
    return proxy_request(url, session)


@app.get("/providers/{provider}/categories/{slug}", tags=["Categories"])
def get_category_detail(
    provider: str = Path(..., description="The provider name, e.g. 'maktabkhooneh'"),
    slug: str = Path(..., description="The category slug to fetch"),
    session: requests.Session = Depends(get_http_client),
) -> JSONResponse:
    """Retrieve details for a single category from the specified provider.

    This proxies the provider's ``/categories/{slug}/`` route.  The
    upstream returns metadata about the category (e.g. title,
    description and child categories).
    """
    config = get_provider_config(provider)
    url = f"{config['base_url']}/{slug}/"
    return proxy_request(url, session)


@app.get("/providers/{provider}/categories/{slug}/search", tags=["Courses"])
def search_category_courses(
    request: Request,
    provider: str = Path(..., description="The provider name, e.g. 'maktabkhooneh'"),
    slug: str = Path(..., description="The category slug to search for courses"),
    session: requests.Session = Depends(get_http_client),
) -> JSONResponse:
    """Search courses within a category and return the results.

    Query parameters are forwarded to the upstream API unchanged.  For
    example, you can call ``/providers/maktabkhooneh/categories/python/search?limit=12``
    to limit the number of returned items.  The upstream API supports
    paging and sorting parameters.
    """
    config = get_provider_config(provider)
    url = f"{config['base_url']}/{slug}/search/"
    # Forward all query parameters to the upstream API
    query_params = dict(request.query_params)
    return proxy_request(url, session, params=query_params)