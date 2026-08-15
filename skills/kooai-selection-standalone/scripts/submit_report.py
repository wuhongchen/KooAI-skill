#!/usr/bin/env python3
"""Submit one bounded report JSON file to the local standalone service."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


MAX_BYTES = 5 * 1024 * 1024


def trusted_base_url(value: str) -> str:
    parsed = urlsplit(value.rstrip("/"))
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
    return f"http://{parsed.hostname}:{parsed.port}"


def submit_report(base_url: str, report_path: str | Path) -> dict:
    path = Path(report_path)
    payload = path.read_bytes()
    if len(payload) > MAX_BYTES:
        raise ValueError("report exceeds 5 MiB")
    parsed = json.loads(payload)
    if not isinstance(parsed, dict):
        raise ValueError("report must be a JSON object")
    request = Request(
        trusted_base_url(base_url) + "/api/reports",
        data=payload,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    with urlopen(request, timeout=8) as response:
        result = json.load(response)
    if not isinstance(result, dict) or not isinstance(result.get("item"), dict):
        raise RuntimeError("local service returned an invalid response")
    return result["item"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit a standalone selection report")
    parser.add_argument("report_path")
    parser.add_argument("--base-url", default="http://127.0.0.1:8765")
    args = parser.parse_args()
    item = submit_report(args.base_url, args.report_path)
    print(json.dumps({"report_id": item["report_id"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
