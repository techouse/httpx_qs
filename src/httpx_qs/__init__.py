"""httpx-qs: A library for smart query string handling with httpx."""

__version__ = "0.2.1"

from .enums.merge_policy import MergePolicy
from .transporters import smart_query_strings
from .utils.merge_query import merge_query


__all__ = [
    "smart_query_strings",
    "MergePolicy",
    "merge_query",
]
