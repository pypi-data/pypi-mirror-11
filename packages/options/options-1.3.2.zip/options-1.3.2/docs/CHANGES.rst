Change Log
==========

**1.3.2**  (August 26, 2015)

    Reorganized documentation structure.


**1.3.0**  (August 25, 2015)

    Added test branch metrics to coverage evaluation. Line coverage
    now 93%; branch coverage 92%.

    Integrated reading/writing of options data to JSON files now
    operational and tested.


**1.2.5**  (August 17, 2015)

    Inaugurated automated test coverage analysis. Extended a few tests
    and cleaned up some code as a result. Published with coverage at
    88%.


**1.2.2**  (August 11, 2015)

    Simplified setup.


**1.2.1**  (August 4, 2015)

    Added wheel distribution format. Updated test matrix.

    Moved from BSD to Apache Software License.

    Moved status to production/stable from beta.


**1.2.0**  (July 22, 2015)

    Doc and config tweaks.

    Python 2.6 support wavering, primarily because of failure of
    ``stuf`` 0.9.16 to build there. 0.9.14 works fine. But either
    ``stuf`` support will have to improve (I've submitted a pull
    request that fixes the problem), or we'll have to swap ``stuf``
    out, or we''ll have to decomit py26.


**1.1.7**  (December 16, 2014)

    Added snazzy badges to PyPI readme


**1.1.5**  (December 16, 2014)

    Changed dependencies to utilize new ``nulltype`` package
    (unbundling it). Ensured tested on all lastest Python versions.


**1.1.1**  (October 29, 2013)

    Added ``OptionsClass`` base class. If client classes inherit from
    this, they automatically get ` set()`` and ``settings()`` methods.


**1.0.7**  (October 25, 2103)

    Mainly doc tweaks.


**1.0.4**  (October 24, 2013)

    When bad option names are defined ("bad" here meaning "conflicts
    with names already chosen for pre-existing methods"), a
    ``BadOptionName`` exception will be raised.

    Tweaked docs, adding comparison chart.


**1.0.3**  (September 23, 2013)

    Switched to local version of ``chainstuf`` until bug with
    generator values in ``stuf.chainstuf`` can be tracked down and
    corrected. This was blocking a downstream feature-release of
    ``say``.


**1.0.2**  (September 19, 2013)

    Improved ``setdefault`` and ``update`` methods, and added tests,
    primarily in effort to work around bug that appears in ``stuf``,
    ``orderedstuf``, or ``chainstuf`` when a mapping value is a
    generator.

    Documentation improved.


**1.0.1**  (September 14, 2013)

    Moved main documentation to Sphinx format in ./docs, and hosted
    the long-form documentation on readthedocs.org. README.rst now an
    abridged version/teaser for the module.


**1.0.0**  (September 10, 2013)

    Cleaned up source for better PEP8 conformance

    Bumped version number to 1.0 as part of move to `semantic
    versioning <http://semver.org>`_, or at least enough of it so as
    to not screw up Python installation procedures (which don't seem
    to understand 0.401 is a lesser version that 0.5, because 401 >
    5).



