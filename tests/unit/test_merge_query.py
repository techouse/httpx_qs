import pytest

from httpx_qs import MergePolicy, merge_query


class TestMergeQuery:
    def setup_method(self) -> None:  # noqa: D401 - simple state holder setup
        self.base_existing = "https://example.com?a=1"

    def teardown_method(self) -> None:  # noqa: D401 - no resources to release
        # Placeholder for symmetry / future resource cleanup
        pass

    @pytest.mark.parametrize(
        "policy,expected",
        [
            (MergePolicy.COMBINE, "a=1&a=2"),
            (MergePolicy.REPLACE, "a=2"),
            (MergePolicy.KEEP, "a=1"),
        ],
    )
    def test_merge_policies(self, policy: MergePolicy, expected: str) -> None:
        result = merge_query(self.base_existing, {"a": 2}, policy=policy)
        assert result.endswith(expected)

    def test_merge_error_policy(self) -> None:
        with pytest.raises(ValueError):
            merge_query(self.base_existing, {"a": 2}, policy=MergePolicy.ERROR)

    def test_merge_new_keys(self) -> None:
        result = merge_query(self.base_existing, {"b": 2})
        assert result.endswith("a=1&b=2") or result.endswith("b=2&a=1")
