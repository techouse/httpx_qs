httpx-qs
========

Smart, policy-driven query string merging & encoding for `httpx <https://www.python-httpx.org>`_ powered by
`qs-codec <https://techouse.github.io/qs_codec/>`_.

.. image:: https://img.shields.io/pypi/v/httpx-qs?logo=pypi
   :target: https://pypi.org/project/httpx-qs/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/status/httpx-qs?logo=pypi
   :target: https://pypi.org/project/httpx-qs/
   :alt: PyPI - Status

.. image:: https://img.shields.io/pypi/pyversions/httpx-qs?logo=python&label=Python
   :target: https://pypi.org/project/httpx-qs/
   :alt: Supported Python versions

.. image:: https://img.shields.io/badge/PyPy-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-6f42c1?logo=pypy
   :target: https://www.pypy.org/
   :alt: PyPy support status

.. image:: https://img.shields.io/pypi/format/httpx-qs?logo=python
   :target: https://pypi.org/project/httpx-qs/
   :alt: PyPI - Format

.. image:: https://github.com/techouse/httpx_qs/actions/workflows/test.yml/badge.svg
   :target: https://github.com/techouse/httpx_qs/actions/workflows/test.yml
   :alt: Tests

.. image:: https://github.com/techouse/httpx_qs/actions/workflows/github-code-scanning/codeql/badge.svg
   :target: https://github.com/techouse/httpx_qs/actions/workflows/github-code-scanning/codeql
   :alt: CodeQL

.. image:: https://img.shields.io/github/license/techouse/httpx_qs
   :target: https://github.com/techouse/httpx_qs/blob/master/LICENSE
   :alt: License

.. image:: https://codecov.io/gh/techouse/httpx_qs/graph/badge.svg?token=JMt8akIZFh
   :target: https://codecov.io/gh/techouse/httpx_qs
   :alt: Codecov

.. image:: https://app.codacy.com/project/badge/Grade/420bf66ab90d4b3798573b6ff86d02af
   :target: https://app.codacy.com/gh/techouse/httpx_qs/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade
   :alt: Codacy Quality

.. image:: https://img.shields.io/github/sponsors/techouse?logo=github
   :target: https://github.com/sponsors/techouse
   :alt: GitHub Sponsors

.. image:: https://img.shields.io/github/stars/techouse/httpx_qs
   :target: https://github.com/techouse/httpx_qs/stargazers
   :alt: GitHub Repo stars

.. image:: https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg?logo=contributorcovenant
   :target: CODE-OF-CONDUCT.md
   :alt: Contributor Covenant

.. |flake8| image:: https://img.shields.io/badge/flake8-checked-blueviolet.svg?logo=python
   :target: https://flake8.pycqa.org/en/latest/

.. image:: https://img.shields.io/badge/mypy-checked-blue.svg?logo=python
   :target: https://mypy.readthedocs.io/en/stable/
   :alt: mypy

.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen.svg?logo=python
   :target: https://github.com/pylint-dev/pylint
   :alt: pylint

.. image:: https://img.shields.io/badge/imports-isort-blue.svg?logo=python
   :target: https://pycqa.github.io/isort/
   :alt: isort

.. image:: https://img.shields.io/badge/security-bandit-blue.svg?logo=python
   :target: https://github.com/PyCQA/bandit
   :alt: Security Status

Overview
--------

``httpx-qs`` provides:

* A transport wrapper ``SmartQueryStrings`` that merges *existing* URL query parameters with *additional* ones supplied via ``request.extensions``.
* A flexible ``merge_query`` utility with selectable conflict resolution policies.
* Consistent, standards-aware encoding via ``qs-codec`` (RFC3986 percent-encoding, structured arrays, nested objects, etc.).

Why?
----

HTTPX already lets you pass ``params=`` when making requests, but sometimes you need to:

* Inject **additional** query parameters from middleware/transport layers (e.g., auth tags, tracing IDs, feature flags) *without losing* the caller's original intent.
* Combine repeated keys or treat them deterministically (replace / keep / error) rather than always flattening.
* Support nested data or list semantics consistent across clients and services.

``qs-codec`` supplies the primitives (decoding & encoding with configurable ``ListFormat``). ``httpx-qs`` stitches that into HTTPX's transport pipeline so you can declaratively extend queries at request dispatch time.

Requirements
------------

* CPython 3.8-3.14 or PyPy 3.8-3.11
* ``httpx>=0.28.1,<1.0.0``
* ``qs-codec>=1.3.1``

Installation
------------

.. code-block:: bash

    pip install httpx-qs

Minimal Example
---------------

.. code-block:: python

    import httpx
    from httpx_qs.transporters.smart_query_strings import SmartQueryStrings

    client = httpx.Client(transport=SmartQueryStrings(httpx.HTTPTransport()))

    response = client.get(
        "https://www.google.com",
        params={"a": "b", "c": "d"},
        extensions={"extra_query_params": {"c": "D", "tags": ["x", "y"]}},
    )

    print(str(response.request.url))
    # Example (order may vary): https://www.google.com/?a=b&c=d&c=D&tags=x&tags=y


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   README
   modules
