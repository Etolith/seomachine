"""Report readiness without provider calls, package installation or secret output."""

import importlib.util
import importlib.metadata
import json
import os
from pathlib import Path
import sys


def readiness():
    packages = {}
    for module, distribution in {
        "textstat": "textstat", "numpy": "numpy", "sklearn": "scikit-learn",
        "requests": "requests", "dotenv": "python-dotenv",
        "google.analytics.data_v1beta": "google-analytics-data",
        "googleapiclient": "google-api-python-client",
    }.items():
        try:
            available = importlib.util.find_spec(module) is not None
        except (ModuleNotFoundError, ValueError):
            available = False
        try:
            version = importlib.metadata.version(distribution) if available else None
        except importlib.metadata.PackageNotFoundError:
            version = None
        packages[distribution] = {"installed": available, "version": version}
    return {
        "python": {"version": sys.version.split()[0], "supported": sys.version_info >= (3, 11)},
        "local_core": "ready" if sys.version_info >= (3, 11) else "unsupported_python",
        "packages": packages,
        "context_files": {name: (Path.cwd() / "context" / name).is_file()
                          for name in ("brand-voice.md", "features.md", "target-keywords.md")},
        "environment_configuration": {
            "dataforseo": all(os.getenv(key) for key in ("DATAFORSEO_LOGIN", "DATAFORSEO_PASSWORD")),
            "ga4": bool(os.getenv("GA4_PROPERTY_ID")),
            "gsc": bool(os.getenv("GSC_SITE_URL")),
            "wordpress": all(os.getenv(key) for key in ("WORDPRESS_URL", "WORDPRESS_USERNAME", "WORDPRESS_APP_PASSWORD")),
        },
        "host_managed_connections": "inspect_with_host_tools",
        "provider_access_verified": False,
    }


if __name__ == "__main__":
    result = readiness()
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["python"]["supported"] else 1)
