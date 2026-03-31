Using Merge Policies
--------------------

Conflict resolution when a key already exists is controlled by ``MergePolicy``.

Available policies:

* ``combine`` (default): concatenate values → existing first, new afterward (``a=1&a=2``)
* ``replace``: last-wins, existing value is overwritten (``a=2``)
* ``keep``: first-wins, ignore the new value (``a=1``)
* ``error``: raise ``ValueError`` on duplicate key

Specify per request:

.. code-block:: python

	from httpx_qs import MergePolicy

	r = client.get(
		"https://api.example.com/resources",
		params={"dup": "original"},
		extensions={
			"extra_query_params": {"dup": "override"},
			"extra_query_params_policy": MergePolicy.REPLACE,
		},
	)
	# Query contains only dup=override

Async Usage
-----------

``SmartQueryStrings`` works equally for ``AsyncClient``:

.. code-block:: python

	import httpx
	from httpx_qs.transporters.smart_query_strings import SmartQueryStrings

	async def main() -> None:
		async with httpx.AsyncClient(transport=SmartQueryStrings(httpx.AsyncHTTPTransport())) as client:
			r = await client.get(
				"https://example.com/items",
				params={"filters": "active"},
				extensions={"extra_query_params": {"page": 2}},
			)
			print(r.request.url)

	# Run with: asyncio.run(main())

``merge_query`` Utility
-----------------------

You can use the underlying function directly:

.. code-block:: python

	from httpx_qs import merge_query, MergePolicy
	from qs_codec import EncodeOptions, ListFormat

	new_url = merge_query(
		"https://example.com?a=1",
		{"a": 2, "tags": ["x", "y"]},
		options=EncodeOptions(list_format=ListFormat.REPEAT),
		policy=MergePolicy.COMBINE,
	)
	# → https://example.com/?a=1&a=2&tags=x&tags=y

Why ``ListFormat.REPEAT`` by Default?
-------------------------------------

``qs-codec`` exposes several list formatting strategies (e.g. repeat, brackets, indices). ``httpx-qs`` defaults to
``ListFormat.REPEAT`` because:

* It matches common server expectations (``key=value&key=value``) without requiring bracket parsing logic.
* It preserves original ordering while remaining unambiguous and simple for log inspection.
* Many API gateways / proxies / caches reliably forward repeated keys whereas bracket syntaxes can be normalized away.

If your API prefers another convention (e.g. ``tags[]=x&tags[]=y`` or ``tags[0]=x``) just pass a custom ``EncodeOptions`` via
``extensions['extra_query_params_options']`` or parameter ``options`` when calling ``merge_query`` directly.

Advanced Per-Request Customization
----------------------------------

.. code-block:: python

	from qs_codec import EncodeOptions, ListFormat

	r = client.get(
		"https://service.local/search",
		params={"q": "test"},
		extensions={
			"extra_query_params": {"debug": True, "tags": ["alpha", "beta"]},
			"extra_query_params_policy": "combine",  # also accepts string values
			"extra_query_params_options": EncodeOptions(list_format=ListFormat.BRACKETS),
		},
	)
	# Example: ?q=test&debug=true&tags[]=alpha&tags[]=beta

Error Policy Example
--------------------

.. code-block:: python

	try:
		client.get(
			"https://example.com",
			params={"token": "abc"},
			extensions={
				"extra_query_params": {"token": "xyz"},
				"extra_query_params_policy": "error",
			},
		)
	except ValueError as exc:
		print("Duplicate detected:", exc)

Testing Strategy
----------------

The project includes unit tests covering policy behaviors, error handling, and transport-level integration. Run them with:

.. code-block:: bash

	pytest

Further Reading
---------------

* HTTPX documentation: https://www.python-httpx.org
* qs-codec documentation: https://techouse.github.io/qs_codec/

License
-------

BSD-3-Clause. See ``LICENSE`` for details.

Contributing
------------

Issues & PRs welcome. Please add tests for new behavior and keep doc examples in sync.
