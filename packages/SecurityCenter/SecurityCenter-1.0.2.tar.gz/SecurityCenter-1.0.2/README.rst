Python wrapper for Tenable SecurityCenter API
=============================================

A powerful wrapper around the SecurityCenter API.
Manages authentication, building requests, and interpreting responses.
Supports the full, unpublished API, above the limited API officially documented.
The "module::action" pattern of the API is represented as dotted access to attributes and methods on the client.

Install::

    $ pip install SecurityCenter

Use::

    >>> from securitycenter import Client
    >>> client = Client('https://localhost:443', 'user', 'password', 'cert_file.crt')
    >>> scan_results = client.scan_result.init()

Many actions return more than the specifically requested data.  For example, ``scanResult::init`` returns information
including users and scanners as well.  Many methods are configured to extract the most common value (in the example, the
scan results).  If a method extracts a value by default, pass ``_key=None`` to return the full response instead. ::

    >>> response = client.scan_result.init(_key=None)
    >>> response.keys()  # all keys returned by method

Some actions return chunks of results.  The library standardizes how paginated requests are made to always use ``page``
and ``page_size`` arguments, and the results become a special pagination object that can iterate over
subsequent pages. ::

    >>> p3 = client.scan_result.get_page(page=3, page_size=10)  # 3rd page, where each page has 10 items
    >>> p3  # list of items on current page
    >>> p4 = p1.next_page()  # make request for next page
    >>> pages = list(p1.iter_pages())  # all pages
    >>> items = list(p1.iter_items())  # all items

.. note:: Only the modules and actions that I actually use in my own projects have been implemented.  I'm willing to
    implement or accept patches to support other methods, but won't be proactive about implementing them.  Please open
    an issue on the BitBucket repo to request or add more methods.

Links
-----

* `PyPI releases <https://pypi.python.org/pypi/securitycenter>`_
* `Source code <https://bitbucket.org/davidism/securitycenter>`_
