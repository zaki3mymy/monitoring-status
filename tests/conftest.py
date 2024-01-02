import json
import os

import pytest


@pytest.fixture(autouse=True)
def setenv(monkeypatch):
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path) as f:
        config = json.load(f)

    monkeypatch.setenv("SECRET_KEY", config["SECRET_KEY"])
    monkeypatch.setenv("DATABASE_ID", config["DATABASE_ID"])
    monkeypatch.setenv("PROPERTY_NAME_STATUS", "Status")
    monkeypatch.setenv("PROPERTY_VALUE_STATUS_DONE", "Done")
    monkeypatch.setenv("PROPERTY_NAME_PUBLISH", "Publish")
