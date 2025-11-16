#!/usr/bin/env python3
"""
SAP Alias Redirect Service

Provides HTTP redirects and API endpoints for legacy SAP-XXX identifiers
to modern chora.domain.capability namespace format.

Features:
- HTTP 301 redirects: /SAP-XXX -> modern namespace documentation
- REST API: /api/v1/resolve/{sap_id} -> JSON response with modern namespace
- Deprecation warnings in all responses
- Sunset timeline tracking (2026-06-01)

Usage:
    # Development
    uvicorn app:app --reload --port 8000

    # Production
    uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4

API Endpoints:
    GET /SAP-XXX                    - HTTP 301 redirect to namespace docs
    GET /api/v1/resolve/{sap_id}    - JSON response with namespace
    GET /api/v1/aliases             - List all aliases
    GET /health                     - Health check
    GET /                           - API documentation
"""

import json
from datetime import datetime, date
from pathlib import Path
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel

# Constants
ALIAS_MAPPING_PATH = Path(__file__).parent.parent.parent / "capabilities" / "alias-mapping.json"
SUNSET_DATE = date(2026, 6, 1)
DOCS_BASE_URL = "https://github.com/chora-base/chora-base/blob/main/docs/skilled-awareness"

# Models
class AliasInfo(BaseModel):
    """Alias information"""
    sap_id: str
    namespace: str
    status: str
    sunset_date: str
    deprecated: bool
    days_until_sunset: int


class ResolveResponse(BaseModel):
    """API response for alias resolution"""
    sap_id: str
    namespace: str
    status: str
    sunset_date: str
    deprecated: bool
    days_until_sunset: int
    deprecation_warning: str
    docs_url: str
    migration_guide_url: str


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    message: str
    available_aliases: Optional[list] = None


# Application
app = FastAPI(
    title="SAP Alias Redirect Service",
    description="Legacy SAP-XXX identifier resolution service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Global alias mapping cache
_alias_cache: Dict[str, Dict] = {}


def load_alias_mapping() -> Dict[str, Dict]:
    """Load alias mapping from JSON file"""
    if not ALIAS_MAPPING_PATH.exists():
        raise FileNotFoundError(f"Alias mapping not found: {ALIAS_MAPPING_PATH}")

    with open(ALIAS_MAPPING_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("aliases", {})


def get_days_until_sunset() -> int:
    """Calculate days until sunset date"""
    today = date.today()
    delta = SUNSET_DATE - today
    return max(0, delta.days)


def get_deprecation_warning(days_until_sunset: int) -> str:
    """Generate deprecation warning message"""
    if days_until_sunset == 0:
        return (
            "⚠️ DEPRECATED: Legacy SAP-XXX identifiers are no longer supported. "
            "Please use modern chora.domain.capability namespaces immediately."
        )
    elif days_until_sunset <= 30:
        return (
            f"⚠️ CRITICAL: Legacy SAP-XXX identifiers will be sunset in {days_until_sunset} days. "
            "Please migrate to modern chora.domain.capability namespaces immediately."
        )
    elif days_until_sunset <= 90:
        return (
            f"⚠️ WARNING: Legacy SAP-XXX identifiers will be sunset in {days_until_sunset} days. "
            "Please plan migration to modern chora.domain.capability namespaces."
        )
    else:
        return (
            f"ℹ️ NOTICE: Legacy SAP-XXX identifiers are deprecated and will be sunset on {SUNSET_DATE}. "
            "Please migrate to modern chora.domain.capability namespaces."
        )


def get_docs_url(namespace: str) -> str:
    """Generate documentation URL for namespace"""
    # Extract capability name from namespace (e.g., chora.devex.bootstrap -> bootstrap)
    parts = namespace.split(".")
    if len(parts) >= 3:
        capability = parts[2].replace("_", "-")
        return f"{DOCS_BASE_URL}/{capability}/"
    return DOCS_BASE_URL


@app.on_event("startup")
async def startup_event():
    """Load alias mapping on startup"""
    global _alias_cache
    _alias_cache = load_alias_mapping()
    print(f"Loaded {len(_alias_cache)} alias mappings")


@app.get("/", response_class=JSONResponse)
async def root():
    """API documentation and service info"""
    days_until_sunset = get_days_until_sunset()

    return {
        "service": "SAP Alias Redirect Service",
        "version": "1.0.0",
        "status": "active",
        "deprecation_notice": get_deprecation_warning(days_until_sunset),
        "sunset_date": str(SUNSET_DATE),
        "days_until_sunset": days_until_sunset,
        "total_aliases": len(_alias_cache),
        "endpoints": {
            "redirect": "GET /{sap_id} - HTTP 301 redirect to namespace docs",
            "resolve": "GET /api/v1/resolve/{sap_id} - JSON response with namespace",
            "aliases": "GET /api/v1/aliases - List all aliases",
            "health": "GET /health - Health check",
            "docs": "GET /docs - OpenAPI documentation",
        },
        "migration_guide": "https://github.com/chora-base/chora-base/blob/main/docs/ontology/migration-guide.md",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "aliases_loaded": len(_alias_cache),
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/api/v1/aliases", response_model=Dict[str, AliasInfo])
async def list_aliases():
    """List all available aliases"""
    days_until_sunset = get_days_until_sunset()

    aliases = {}
    for sap_id, info in _alias_cache.items():
        aliases[sap_id] = AliasInfo(
            sap_id=sap_id,
            namespace=info["namespace"],
            status=info.get("status", "deprecated"),
            sunset_date=info.get("sunset_date", str(SUNSET_DATE)),
            deprecated=True,
            days_until_sunset=days_until_sunset,
        )

    return aliases


@app.get("/api/v1/resolve/{sap_id}", response_model=ResolveResponse)
async def resolve_alias(sap_id: str):
    """
    Resolve SAP-XXX identifier to modern namespace

    Returns JSON with:
    - Modern namespace
    - Deprecation status
    - Documentation URLs
    - Migration guidance
    """
    # Normalize SAP ID (handle with or without "SAP-" prefix)
    if not sap_id.startswith("SAP-"):
        sap_id = f"SAP-{sap_id}"

    sap_id = sap_id.upper()

    # Lookup alias
    if sap_id not in _alias_cache:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "not_found",
                "message": f"SAP identifier '{sap_id}' not found",
                "available_aliases": sorted(_alias_cache.keys())[:10],
            }
        )

    alias_info = _alias_cache[sap_id]
    namespace = alias_info["namespace"]
    days_until_sunset = get_days_until_sunset()

    return ResolveResponse(
        sap_id=sap_id,
        namespace=namespace,
        status=alias_info.get("status", "deprecated"),
        sunset_date=alias_info.get("sunset_date", str(SUNSET_DATE)),
        deprecated=True,
        days_until_sunset=days_until_sunset,
        deprecation_warning=get_deprecation_warning(days_until_sunset),
        docs_url=get_docs_url(namespace),
        migration_guide_url="https://github.com/chora-base/chora-base/blob/main/docs/ontology/migration-guide.md",
    )


@app.get("/{sap_id}")
async def redirect_to_docs(sap_id: str):
    """
    HTTP 301 redirect from SAP-XXX to modern namespace documentation

    This endpoint provides backward compatibility for legacy SAP-XXX URLs.
    Clients will be redirected to the modern namespace documentation with
    a deprecation warning header.
    """
    # Normalize SAP ID
    if not sap_id.startswith("SAP-"):
        sap_id = f"SAP-{sap_id}"

    sap_id = sap_id.upper()

    # Lookup alias
    if sap_id not in _alias_cache:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "not_found",
                "message": f"SAP identifier '{sap_id}' not found",
                "hint": "Use /api/v1/aliases to see available aliases",
            }
        )

    alias_info = _alias_cache[sap_id]
    namespace = alias_info["namespace"]
    docs_url = get_docs_url(namespace)
    days_until_sunset = get_days_until_sunset()

    # Create redirect response with deprecation headers
    response = RedirectResponse(
        url=docs_url,
        status_code=301,  # Permanent redirect
    )

    # Add deprecation headers
    response.headers["X-Deprecated"] = "true"
    response.headers["X-Sunset-Date"] = str(SUNSET_DATE)
    response.headers["X-Days-Until-Sunset"] = str(days_until_sunset)
    response.headers["X-Modern-Namespace"] = namespace
    response.headers["X-Deprecation-Warning"] = get_deprecation_warning(days_until_sunset)
    response.headers["X-Migration-Guide"] = "https://github.com/chora-base/chora-base/blob/main/docs/ontology/migration-guide.md"

    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
