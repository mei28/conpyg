from conpyg import Config
import yaml
from hypothesis import given, strategies as st

leaf = st.booleans() | st.integers() | st.floats(allow_nan=False) | st.text()

nested_dicts = st.recursive(
    st.dictionaries(st.text(min_size=1), leaf, max_size=4),
    lambda children: st.dictionaries(st.text(min_size=1), children, max_size=4),
    max_leaves=10,
)


def roundtrip(cfg: Config) -> Config:
    """pretty() → YAML 文字列 → dict → Config で値が保たれるか"""
    dumped = cfg.pretty(sort_keys=True)  # YAML str
    reloaded = Config(yaml.safe_load(dumped))  # back to Config
    return reloaded


@given(data=nested_dicts)
def test_pretty_roundtrip(data):
    cfg = Config(data)
    assert roundtrip(cfg).to_dict() == cfg.to_dict()


def test_pretty_human(sample_dict):
    cfg = Config(sample_dict)
    text = cfg.pretty()
    # 簡単な目視用 assert
    assert "db:" in text
    assert "host:" in text
