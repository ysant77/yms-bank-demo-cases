"""Front-end checks that need no browser: static serving and a small CSS parse."""

import re
from pathlib import Path

from fastapi.testclient import TestClient

from bank.api import WEB_DIR, create_app


def test_pages_are_served_without_external_assets(tmp_path):
    client = TestClient(create_app(tmp_path / "web.db", seed_if_empty=False))
    page = client.get("/")
    assert page.status_code == 200
    assert "YMS Bank" in page.text and 'id="send-button"' in page.text
    for asset in ("/app.css", "/app.js"):
        assert client.get(asset).status_code == 200
    for path in Path(WEB_DIR).iterdir():
        text = path.read_text(encoding="utf-8")
        assert not re.search(r"(src|href)=\"(https?:)?//", text), path.name
        assert "@import" not in text and "url(http" not in text, path.name
