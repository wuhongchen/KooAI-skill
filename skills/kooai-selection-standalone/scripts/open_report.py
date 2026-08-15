#!/usr/bin/env python3
"""Open one validated report ID in the local standalone page."""

from __future__ import annotations

import argparse
import re
import webbrowser
from urllib.parse import urlsplit


REPORT_ID = re.compile(r"^[A-Za-z0-9_-]{1,160}$")


def report_url(report_id: str, base_url: str = "http://127.0.0.1:8765") -> str:
    if not REPORT_ID.fullmatch(report_id):
        raise ValueError("invalid report ID")
    parsed = urlsplit(base_url.rstrip("/"))
    if (
        parsed.scheme != "http"
        or parsed.hostname not in {"127.0.0.1", "localhost"}
        or parsed.port is None
        or parsed.username
        or parsed.password
        or parsed.path
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("base URL must be an explicit local loopback HTTP address")
    return f"http://{parsed.hostname}:{parsed.port}/reports/{report_id}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Open a standalone selection report")
    parser.add_argument("report_id")
    parser.add_argument("--base-url", default="http://127.0.0.1:8765")
    args = parser.parse_args()
    webbrowser.open(report_url(args.report_id, args.base_url))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
