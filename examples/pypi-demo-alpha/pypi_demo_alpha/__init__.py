"""
pypi-demo-alpha: SAP-028 OIDC Publishing Demonstration Package (Alpha)

This is a minimal demonstration package showcasing SAP-028 (Publishing Automation)
with OIDC trusted publishing to PyPI.

Key features demonstrated:
- Zero-secret publishing using OIDC trust relationship (GitHub → PyPI)
- PEP 740 attestations for build provenance
- Secure-by-default configuration
- 5-minute setup time (L3 maturity metric)
"""

__version__ = "0.1.0"

def hello_sap028():
    """
    Simple function demonstrating SAP-028 adoption.

    Returns:
        str: Greeting message confirming SAP-028 publishing
    """
    return (
        "Hello from pypi-demo-alpha! "
        "Published to PyPI using SAP-028 OIDC trusted publishing. "
        "Zero secrets, PEP 740 attestations enabled."
    )


__all__ = ["hello_sap028", "__version__"]
