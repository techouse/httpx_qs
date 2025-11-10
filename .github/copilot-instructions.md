# httpx-qs • Copilot Guide

## Big picture
- Library wraps HTTPX transports; `SmartQueryStrings` merges URL queries using `qs_codec` before handing off to `next_transport`.
- Core surface lives in `src/httpx_qs/`: `transporters/smart_query_strings.py`, `utils/merge_query.py`, and the enum in `enums/merge_policy.py` (exported via `__init__.py`).
- Query merging relies on `qs_codec.encode/decode`; default `EncodeOptions(list_format=ListFormat.REPEAT)` keeps repeated keys ordered and predictable.
- Extra params are fed through `request.extensions` keys: `extra_query_params`, optional `extra_query_params_policy`, and `extra_query_params_options`.

## Implementation patterns
- Always treat the decoded query as immutable input—use `_combine` to copy list values before concatenating.
- `MergePolicy` accepts both enum values and strings; validate via `MergePolicy(policy)` the way `merge_query` does.
- Keep public APIs typed; `py.typed` ships with the wheel, so avoid `Any` on exported functions.
- When adding transports, ensure they proxy every HTTPX `handle_request` call to the wrapped transport without swallowing responses.
- Update `__version__` in `src/httpx_qs/__init__.py` alongside changelog entries; Hatch reads the version from this file.

## Tests & quality checks
- Unit tests live in `tests/unit/` and mirror module layout; they use class-based fixtures (`setup_method` / `teardown_method`).
- Fast feedback: `pytest` (configured with `-rsxX -l --tb=short --strict-markers`).
- Full matrix: `tox -p` (runs multi-Python plus lint/type/doc stacks); individual envs include `tox -e linters`, `tox -e mypy`, etc.
- Coverage target is 100%—new logic should have explicit tests, especially for merge branches (`combine/replace/keep/error`).
- Format with Black (120 cols) and check imports with isort (profile=black); lint via Flake8/Pylint/Bandit when touching core modules.

## Docs & packaging
- Sphinx sources live in `docs/`; `docs/index.rst` mirrors `README.rst` and `docs/modules.rst` drives autodoc stubs under `docs/api/`.
- When creating new modules, add matching `docs/api/<module>.rst` entries so the toctree stays warning-free and run `tox -e docs` (or `sphinx-build -b html docs docs/_build/html`).
- Shipping build uses Hatch; run `python -m build` for release validation and keep `src/httpx_qs/py.typed` in sync with type hints.
- Tests reference `DummyTransport` for isolation—reuse that pattern when exercising transport behavior without network I/O.

Let me know if any section needs more detail or if project conventions change so we can update this guide.