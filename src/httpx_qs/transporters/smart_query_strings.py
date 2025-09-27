"""A transport that merges extra query params supplied via request.extensions."""

import typing as t

import httpx
from qs_codec import EncodeOptions, ListFormat

from httpx_qs.utils.merge_query import MergePolicy, merge_query


class SmartQueryStrings(httpx.BaseTransport):
    """A transport that merges extra query params supplied via request.extensions."""

    def __init__(self, next_transport: httpx.BaseTransport) -> None:
        """Initialize with the next transport in the chain."""
        self.next_transport = next_transport

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        """Handle the request, merging extra query params if provided."""
        extra_params: t.Dict[t.Any, t.Any] = request.extensions.get("extra_query_params", {})
        extra_params_options: t.Optional[EncodeOptions] = request.extensions.get("extra_query_params_options", None)
        merge_policy: t.Optional[t.Union[MergePolicy, str]] = request.extensions.get("extra_query_params_policy")
        if extra_params:
            request.url = httpx.URL(
                merge_query(
                    str(request.url),
                    extra_params,
                    (
                        extra_params_options
                        if extra_params_options is not None
                        else EncodeOptions(list_format=ListFormat.REPEAT)
                    ),
                    policy=merge_policy if merge_policy is not None else MergePolicy.COMBINE,
                )
            )
        return self.next_transport.handle_request(request)
