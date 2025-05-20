.. only:: prerelease

    .. warning:: This is the documentation for a development version of pushover_complete.

        .. only:: readthedocs

            `Documentation for the Most Recent Stable Version <http://pushover-complete.readthedocs.io/en/stable/>`_

.. _changelog:

Changelog
=========

:mod:`pushover_complete` adheres to the Semantic Versioning ("Semver") 2.0.0 versioning standard.
Details about this versioning scheme can be found on the `Semver website <http://semver.org/spec/v2.0.0.html>`_.
Versions postfixed with '-dev' are currently under development and those without a postfix are stable releases.

Changes as of 20 May 2025

2.0.0 <20 May 2025>
^^^^^^^^^^^^^^^^^^^

- Harden GitHub Actions configurations by removing some template interpolation and adding constraints to the Python dependencies used in CI (`Pull #21 <https://github.com/scolby33/pushover_complete/pull/21>`_)
- Change to using pytest-cov for coverage measurements and fix coverage uploading to Codecov (`Pull #22 <https://github.com/scolby33/pushover_complete/pull/22>`_)
- Minor changes to copyright symbol in license files (`Pull #24 <https://github.com/scolby33/pushover_complete/pull/24>`_)
- Remove Python 2.7 compatability (`Pull #23 <https://github.com/scolby33/pushover_complete/pull/23>`_)

1.2.0 <24 March 2025>
^^^^^^^^^^^^^^^^^^^^^

- Major modernization of the project's supporting structures
- Add Time To Live (TTL) support (`Pull #14 <https://github.com/scolby33/pushover_complete/pull/14>`_)
- Now supporting Python 2.7 and 3.9 to 3.13
- Note: this will be the final release supporting Python 2.7
- Fully replace setup.py with pyproject.toml
- Use GitHub Actions instead of Travis for CI/CD
- Use GitHub Actions for trusted publishing to PyPI
- Various updates to documentation

1.1.1 <6 April 2018>
^^^^^^^^^^^^^^^^^^^^

- HOTFIX for 1.1.0
- Fix Python versions badge in the documents index
- Add the Python 3.6 classifier in :code:`setup.py` so the right versions are shown on PyPI

1.1.0 <6 April 2018>
^^^^^^^^^^^^^^^^^^^^

- Add `image attachment support <https://pushover.net/api#attachments>`_ (Pulls `#5 <https://github.com/scolby33/pushover_complete/pull/5>`_ and `#9 <https://github.com/scolby33/pushover_complete/pull/9>`_)
- Officially add support for Python 3.6
- Officially deprecate support for Python 3.5. It will be removed in the next major version release.
- Change default tox environment for Python 3 to py36
- Refactored :code:`.travis.yml` to be more concise and use the new :code:`py` `environment specification <https://tox.readthedocs.io/en/3.0.0/example/basic.html#a-simple-tox-ini-default-environments>`_ (Pull `#8 <https://github.com/scolby33/pushover_complete/pull/8>`_)
- Some refactoring in the main API (more list comprehensions yay!) (Pull `#6 <https://github.com/scolby33/pushover_complete/pull/6>`_)
- Several small documentation changes/refinements

1.0.2 <23 December 2016>
^^^^^^^^^^^^^^^^^^^^^^^^

- "Add" Python 3.6 support. It's not in Travis as an allowed failure and didn't require any code changes to pass!
- Fix a major bug with the receipt cancel API. I was using a `GET` request instead of a `POST`
- Stop using the `releases` Sphinx plugin for the changelog. Its philosophy didn't match well with mine
- Update release procedure based on no longer using `releases`
- Some minor documentation fixes


1.0.1 <10 May 2016>
^^^^^^^^^^^^^^^^^^^

- Officially add Python 2.7 support and add testing for it to tox and Travis
- Numerous updates to documentation and README, etc. to make them prettier and more useful

1.0.0 <9 May 2016>
^^^^^^^^^^^^^^^^^^

- Implementation of methods for the Pushover messages, sounds, users, receipt, subscriptions, groups, and licenses APIs
- Documentation and build process
