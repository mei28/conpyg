from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
from typing import Any, Iterable

import yaml


# ────────────────────────────────────────────────
# ヘルパ: dict を深くマージ
def _deep_merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    for k, v in patch.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            base[k] = _deep_merge(base[k], v)
        else:
            base[k] = v
    return base


# ────────────────────────────────────────────────
class Config:
    """動的・階層型設定オブジェクト"""

    def __init__(self, data: dict[str, Any] | None = None) -> None:
        # 生 dict を隠蔽
        object.__setattr__(self, "_data", data or {})

    # ========== 取得 ==========
    def __getattr__(self, item: str) -> Any:
        if item in self._data:
            val = self._data[item]
            return Config(val) if isinstance(val, dict) else val
        raise AttributeError(item)

    def __getitem__(self, dotted_key: str) -> Any:
        keys = dotted_key.split(".")
        d: Any = self
        for k in keys:
            d = getattr(d, k)
        return d

    # ========== 設定 ==========
    def __setattr__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def __setitem__(self, dotted_key: str, value: Any) -> None:
        keys = dotted_key.split(".")
        d = self._data
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value

    # ========== ツール ==========
    def merge(self, *others: "Config | dict[str, Any]") -> "Config":
        """self を破壊的に deep-merge"""
        for other in others:
            other_dict = other._data if isinstance(other, Config) else other
            _deep_merge(self._data, other_dict)
        return self

    def copy(self) -> "Config":
        return Config(copy.deepcopy(self._data))

    def to_dict(self) -> dict[str, Any]:
        return copy.deepcopy(self._data)

    # ========== ファイル IO ==========
    @classmethod
    def load(cls, path: str | Path) -> "Config":
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(p)
        if p.suffix in {".yml", ".yaml"}:
            data = yaml.safe_load(p.read_text())
        elif p.suffix == ".json":
            data = json.loads(p.read_text())
        else:
            raise ValueError("Unsupported format")
        return cls(data or {})

    def save(self, path: str | Path) -> None:
        p = Path(path)
        if p.suffix in {".yml", ".yaml"}:
            yaml.safe_dump(self._data, p.open("w"), allow_unicode=True)
        elif p.suffix == ".json":
            json.dump(self._data, p.open("w"), indent=2, ensure_ascii=False)
        else:
            raise ValueError("Unsupported format")

    # ========== CLI ==========
    @classmethod
    def from_cli(
        cls,
        *,
        default_profile: str | Path | None = None,
        extra_args: Iterable[str] | None = None,
    ) -> "Config":
        """
        usage: python main.py --config config/base.yaml --set foo.bar=100 --set debug=true
        """
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--config", default=default_profile)
        parser.add_argument("--set", action="append", default=[], metavar="KEY=VAL")
        known, _ = parser.parse_known_args(extra_args)

        cfg = cls.load(known.config) if known.config else cls()

        for pair in known.set:
            if "=" not in pair:
                raise ValueError(f"--set '{pair}' は KEY=VAL 形式で指定してください")
            k, v_raw = pair.split("=", 1)
            v: Any
            # プリミティブ型をザックリ推定
            if v_raw.lower() in {"true", "false"}:
                v = v_raw.lower() == "true"
            else:
                try:
                    v = int(v_raw)
                except ValueError:
                    try:
                        v = float(v_raw)
                    except ValueError:
                        v = v_raw  # fallback: str
            cfg[k] = v
        return cfg

    # ========== 表示 ==========
    def __repr__(self) -> str:  # pragma: no cover
        return f"Config({self._data})"

    # 末尾付近に追記 ────────────────────────────────────────────
    # ========== Pretty renderer ==========
    def pretty(self, *, sort_keys: bool = False, indent: int = 2) -> str:
        """Return the config as prettified YAML-formatted string."""
        return yaml.safe_dump(
            self.to_dict(),
            sort_keys=sort_keys,
            indent=indent,
            allow_unicode=True,
            default_flow_style=False,
        ).rstrip()  # 末尾改行を揃える

    __str__ = pretty  # print(cfg) で見られるワンライナー
