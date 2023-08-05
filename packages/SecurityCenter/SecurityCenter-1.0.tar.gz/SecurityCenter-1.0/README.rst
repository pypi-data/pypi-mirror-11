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
scan results).  If a method extracts a value by default, pass ``_key=None`` to return the full response instead.

.. note:: Only the modules and actions that I actually use in my own projects have been implemented.  I'm willing to
    implement or accept patches to support other methods, but won't be proactive about implementing them.  Please open
    an issue on the BitBucket repo to request or add more methods.

Links
-----

* `PyPI releases <https://pypi.python.org/pypi/securitycenter>`_
* `Source code <https://bitbucket.org/davidism/securitycenter>`_
