from conpyg import Config
import yaml, json


def test_yaml_load_save(yaml_file, tmp_path):
    cfg = Config.load(yaml_file)
    assert cfg.db.host == "localhost"

    out = tmp_path / "out.yaml"
    cfg.save(out)
    assert yaml.safe_load(out.read_text())["db"]["host"] == "localhost"


def test_json_load_save(json_file, tmp_path):
    cfg = Config.load(json_file)
    assert cfg["list"] == [1, 2, 3]

    out = tmp_path / "out.json"
    cfg.save(out)
    assert json.loads(out.read_text())["list"] == [1, 2, 3]
