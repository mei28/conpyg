import subprocess, sys, json, os, textwrap, yaml
from pathlib import Path
from conpyg import Config


def test_cli_override(tmp_path, yaml_file):
    # テンポラリ main スクリプトを生成
    main_py = tmp_path / "main.py"
    main_py.write_text(
        textwrap.dedent(
            """
            import sys, json
            from conpyg import Config
            cfg = Config.from_cli()
            json.dump(cfg.to_dict(), sys.stdout)
            """
        )
    )
    out = subprocess.check_output([sys.executable, main_py, "--config", yaml_file, "--set", "db.port=9999"])
    result = json.loads(out)
    assert result["db"]["port"] == 9999
