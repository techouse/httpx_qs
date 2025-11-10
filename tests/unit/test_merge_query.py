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
        result: str = merge_query(self.base_existing, {"a": 2}, policy=policy)
        assert result.endswith(expected)

    def test_merge_error_policy(self) -> None:
        with pytest.raises(ValueError):
            merge_query(self.base_existing, {"a": 2}, policy=MergePolicy.ERROR)

    def test_merge_new_keys(self) -> None:
        result: str = merge_query(self.base_existing, {"b": 2})
        assert result.endswith("a=1&b=2") or result.endswith("b=2&a=1")

    def test_merge_list_with_list_combines_both_sides(self) -> None:
        # base URL has repeated key so decode() yields a list for 'a'
        base_with_list: str = "https://example.com?a=1&a=2"
        result: str = merge_query(base_with_list, {"a": ["3", "4"]})
        # Expect four occurrences preserving first two then the added two
        assert result.count("a=") == 4
        assert "a=1" in result and "a=2" in result and "a=3" in result and "a=4" in result

    def test_merge_policy_accepts_string_value(self) -> None:
        result: str = merge_query(self.base_existing, {"a": 2}, policy="replace")
        assert result.endswith("a=2")
