import pytest
from httpx import BaseTransport, Client, Request, Response

from httpx_qs import MergePolicy
from httpx_qs.transporters.smart_query_strings import SmartQueryStrings


class TestTransport:
    client: Client

    def setup_method(self) -> None:
        self.client = Client(transport=SmartQueryStrings(DummyTransport()))

    def teardown_method(self) -> None:
        self.client.close()

    def test_example_usage_combine_default(self) -> None:
        res: Response = self.client.get(
            "https://www.google.com",
            params={"a": "b", "c": "d"},
            extensions={"extra_query_params": {"c": "D", "tags": ["x", "y"]}},
        )
        url_str: str = str(res.request.url)
        # Expect duplicate 'c' values and two tags entries
        assert "a=b" in url_str
        assert url_str.count("c=") == 2  # c=d and c=D
        assert "c=d" in url_str and "c=D" in url_str
        assert url_str.count("tags=") == 2
        assert "tags=x" in url_str and "tags=y" in url_str

    def test_replace_policy(self) -> None:
        res: Response = self.client.get(
            "https://example.com",
            params={"a": "1", "dup": "old"},
            extensions={
                "extra_query_params": {"dup": "new"},
                "extra_query_params_policy": MergePolicy.REPLACE,
            },
        )
        qp: str = str(res.request.url)
        assert "dup=new" in qp and "dup=old" not in qp

    def test_keep_policy(self) -> None:
        res: Response = self.client.get(
            "https://example.com",
            params={"dup": "old"},
            extensions={
                "extra_query_params": {"dup": "new"},
                "extra_query_params_policy": MergePolicy.KEEP,
            },
        )
        qp: str = str(res.request.url)
        # original preserved, new ignored
        assert "dup=old" in qp and "dup=new" not in qp

    def test_error_policy(self) -> None:
        with pytest.raises(ValueError):
            self.client.get(
                "https://example.com",
                params={"dup": "old"},
                extensions={
                    "extra_query_params": {"dup": "new"},
                    "extra_query_params_policy": MergePolicy.ERROR,
                },
            )

    def test_new_keys_added(self) -> None:
        res: Response = self.client.get(
            "https://example.com",
            params={"a": 1},
            extensions={"extra_query_params": {"b": 2}},
        )
        qp: str = str(res.request.url)
        assert "a=1" in qp and "b=2" in qp


class DummyTransport(BaseTransport):
    """A dummy transport that simply returns a 200 response without real I/O."""

    def handle_request(self, request: Request) -> Response:  # type: ignore[override]
        return Response(200, text="ok", request=request)
