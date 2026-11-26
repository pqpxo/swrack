"""SWRack smoke test: run against a running stack (the API needs Postgres).

    RACK_URL=http://localhost:8088 python -m pytest -q tests

Behind SWSuite's login, also set SUITE_USER and SUITE_PASSWORD, eg
RACK_URL=http://<host>:<PORTAL_PORT>/rack. Standard library and pytest only.
"""
import base64
import json
import os
import urllib.request

import pytest

BASE = os.environ.get("RACK_URL", "http://localhost:8088").rstrip("/")
HEADERS = {}
if os.environ.get("SUITE_USER"):
    token = f"{os.environ['SUITE_USER']}:{os.environ.get('SUITE_PASSWORD', '')}".encode()
    HEADERS["Authorization"] = "Basic " + base64.b64encode(token).decode()


def get(path):
    req = urllib.request.Request(BASE + path, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status, r.read()


def test_ui_loads():
    status, body = get("/")
    assert status == 200 and b"<html" in body.lower()


@pytest.mark.parametrize("path", ["/api/cabinets", "/api/equipment-templates", "/api/assets"])
def test_api_lists(path):
    status, body = get(path)
    assert status == 200 and isinstance(json.loads(body), list)
