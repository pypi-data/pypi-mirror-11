
| |version| |downloads| |versions| |impls| |wheel| |coverage| |br-coverage|

.. |version| image:: http://img.shields.io/pypi/v/options.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/options

.. |downloads| image:: http://img.shields.io/pypi/dm/options.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/options

.. |versions| image:: https://img.shields.io/pypi/pyversions/options.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/options

.. |impls| image:: https://img.shields.io/pypi/implementation/options.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/options

.. |wheel| image:: https://img.shields.io/pypi/wheel/options.svg
    :alt: Wheel packaging support
    :target: https://pypi.python.org/pypi/options

.. |coverage| image:: https://img.shields.io/badge/test_coverage-93%25-blue.svg
    :alt: Test line coverage
    :target: https://pypi.python.org/pypi/options

.. |br-coverage| image:: https://img.shields.io/badge/branch_coverage-92%25-blue.svg
    :alt: Test branch coverage
    :target: https://pypi.python.org/pypi/options

``options`` helps represent option and configuration data in a clean,
high-function way. Changes can "overlay" defaults or earlier settings.

For most functions and classes, ``options`` is flexibility overkill. Not
everyone wants or needs to be a world-class gymnast, yogi, or contortionist
For most, Python's regular function arguments, ``*args``, ``**kwargs``, and
inheritance patterns are elegant and sufficient. ``options`` is for the top
1% that need:

  * extremely functional classes, functions, and methods,
  * with many different features and options,
  * the settings for which might be adjusted or overriden at any time,
  * yet that need "reasonable" or "intelligent" defaults, and
  * that yearn for a simple, unobtrusive API.

In those cases, Python's built-in, inheritance-based model stops being the
simple approach. Non-trivial argument-management code code and complexity
begins to pervade. This is where ``options``'s layered, delegation-based
approach begins to shine. Almost regardless of how varied the options it
wrangles, or how much flexibility is required, code complexity remains very
flat.

.. image:: http://content.screencast.com/users/jonathaneunice/folders/Jing/media/15fd180f-a6a8-45ee-a9bb-d99c527b739e/00000742.png
    :align: center

For more backstory, see `this StackOverflow.com discussion of how to combat "configuration sprawl"
<http://stackoverflow.com/questions/11702437/where-to-keep-options-values-paths-to-important-files-etc/11703813#11703813>`_.
``options`` full documentation
can be found at `Read the Docs <http://options.readthedocs.org/en/latest/>`_. For examples of ``options``
in use, see `say <https://pypi.python.org/pypi/say>`_ and `show <https://pypi.python.org/pypi/show>`_.
