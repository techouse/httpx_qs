"""Policy that determines how to handle keys that already exist in the query string."""

from enum import Enum


class MergePolicy(str, Enum):
    """Policy that determines how to handle keys that already exist in the query string.

    Values:
        COMBINE: (default) Combine existing and new values into a list (preserving order: existing then new).
        REPLACE: Replace existing value with the new one (last-wins).
        KEEP: Keep the existing value, ignore the new one (first-wins).
        ERROR: Raise a ValueError if a key collision occurs.
    """

    COMBINE = "combine"
    REPLACE = "replace"
    KEEP = "keep"
    ERROR = "error"
