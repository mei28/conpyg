from conpyg import Config
from hypothesis import given
from hypothesis import strategies as st

# 「トップレベルは必ず dict」にする
leaf = st.integers() | st.text() | st.booleans()
nested_dicts = st.recursive(
    st.dictionaries(st.text(min_size=1), leaf, max_size=4),
    lambda children: st.dictionaries(st.text(min_size=1), children, max_size=4),
    max_leaves=10,
)


@given(base=nested_dicts, patch=nested_dicts)
def test_deep_merge_idempotent(base, patch):
    cfg1 = Config(base).copy()
    cfg1.merge(patch)

    # patch をもう一度マージしても結果は変わらない（冪等性）
    before = cfg1.to_dict()
    cfg1.merge(patch)
    assert cfg1.to_dict() == before
