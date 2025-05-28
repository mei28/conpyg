import json, yaml
from pathlib import Path
import pytest


@pytest.fixture()
def sample_dict():
    return {
        "db": {"host": "localhost", "port": 5432},
        "debug": True,
        "list": [1, 2, 3],
    }


@pytest.fixture()
def yaml_file(tmp_path, sample_dict):
    p = tmp_path / "cfg.yaml"
    yaml.safe_dump(sample_dict, p.open("w"))
    return p


@pytest.fixture()
def json_file(tmp_path, sample_dict):
    p = tmp_path / "cfg.json"
    json.dump(sample_dict, p.open("w"))
    return p
