from conpyg import Config


def test_dot_and_bracket():
    cfg = Config({"a": {"b": {"c": 1}}})
    assert cfg.a.b.c == 1
    assert cfg["a.b.c"] == 1

    cfg["a.b.c"] = 2
    assert cfg.a.b.c == 2
