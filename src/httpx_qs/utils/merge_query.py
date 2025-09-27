"""Utility to merge query parameters into a URL's query string.

Provides different merge policies controlling how conflicting keys are handled.
"""

import typing as t
from urllib.parse import SplitResult, urlsplit, urlunsplit

from qs_codec import EncodeOptions, ListFormat, decode, encode

from httpx_qs.enums.merge_policy import MergePolicy


def _combine(existing_value: t.Any, new_value: t.Any) -> t.List[t.Any]:
    """Return a combined list ensuring list semantics for multiple values.

    Always returns a list (copy) even if both inputs are scalar values.
    """
    left_list: t.List[t.Any]
    if isinstance(existing_value, list):
        # slice copy then cast to satisfy type checker
        left_list = t.cast(t.List[t.Any], existing_value[:])
    else:
        left_list = [existing_value]

    right_list: t.List[t.Any]
    if isinstance(new_value, list):
        right_list = t.cast(t.List[t.Any], new_value[:])
    else:
        right_list = [new_value]
    # Return a new list (avoid mutating originals if lists)
    return list(left_list) + list(right_list)


def merge_query(
    url: str,
    extra: t.Mapping[str, t.Any],
    options: EncodeOptions = EncodeOptions(list_format=ListFormat.REPEAT),
    policy: t.Union[MergePolicy, str] = MergePolicy.COMBINE,
) -> str:
    """Merge extra query parameters into a URL's existing query string.

    Args:
        url: The original URL which may contain an existing query string.
        extra: Mapping of additional query parameters to merge into the URL.
        options: Optional :class:`qs_codec.EncodeOptions` to customize encoding behavior.
        policy: Merge policy to apply when a key already exists (``combine`` | ``replace`` | ``keep`` | ``error``).
    Returns:
        The URL with the merged query string.
    Raises:
        ValueError: If ``policy == 'error'`` and a duplicate key is encountered.
    """
    policy_enum: MergePolicy = MergePolicy(policy) if not isinstance(policy, MergePolicy) else policy

    parts: SplitResult = urlsplit(url)
    existing: t.Dict[str, t.Any] = decode(parts.query) if parts.query else {}

    for k, v in extra.items():
        if k not in existing:
            existing[k] = v
            continue

        # k exists already
        if policy_enum is MergePolicy.COMBINE:
            existing[k] = _combine(existing[k], v)
        elif policy_enum is MergePolicy.REPLACE:
            existing[k] = v
        elif policy_enum is MergePolicy.KEEP:
            # Leave existing value untouched
            continue
        elif policy_enum is MergePolicy.ERROR:
            raise ValueError(f"Duplicate query parameter '{k}' encountered while policy=error")
        else:  # pragma: no cover - defensive (should not happen due to Enum validation)
            existing[k] = _combine(existing[k], v)

    return urlunsplit(
        (
            parts.scheme,
            parts.netloc,
            parts.path,
            encode(existing, options),
            parts.fragment,
        )
    )
