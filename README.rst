pushover_complete
=================
A Python package for interacting with *all* aspects of the Pushover API.

=========== =============== ================== ======================= ====================
Stable      |stable_build|  |stable_coverage|  |stable_documentation|  |stable_pyversions|
Development |develop_build| |develop_coverage| |develop_documentation| |develop_pyversions|
=========== =============== ================== ======================= ====================

.. |stable_build| image:: https://travis-ci.org/scolby33/pushover_complete.svg?branch=master
    :target: https://travis-ci.org/scolby33/pushover_complete
    :alt: Stable Build Status
.. |stable_coverage| image:: https://codecov.io/github/scolby33/pushover_complete/coverage.svg?branch=master
    :target: https://codecov.io/gh/scolby33/pushover_complete/branch/master
    :alt: Stable Test Coverage Status
.. |stable_documentation| image:: http://readthedocs.org/projects/pushover-complete/badge/?version=stable
    :target: http://pushover-complete.readthedocs.io/en/stable/?badge=stable
    :alt: Stable Documentation Status
.. |stable_pyversions| image:: https://img.shields.io/badge/python-2.7%2C%203.5%2C%203.6-blue.svg
    :alt: Stable Supported Python Versions


.. |develop_build| image:: https://travis-ci.org/scolby33/pushover_complete.svg?branch=develop
    :target: https://travis-ci.org/scolby33/pushover_complete
    :alt: Development Build Status
.. |develop_coverage| image:: https://codecov.io/github/scolby33/pushover_complete/coverage.svg?branch=develop
    :target: https://codecov.io/gh/scolby33/pushover_complete/branch/develop
    :alt: Development Test Coverage Status
.. |develop_documentation| image:: http://readthedocs.org/projects/pushover-complete/badge/?version=develop
    :target: http://pushover-complete.readthedocs.io/en/develop/?badge=develop
    :alt: Development Documentation Status
.. |develop_pyversions| image:: https://img.shields.io/badge/python-2.7%2C%203.5%2C%203.6-blue.svg
    :alt: Development Supported Python Versions

To learn more about Pushover and the Pushover API, please visit the Pushover Website, `<https://pushover.net>`_.

.. code-block:: python

   >>> from pushover_complete import PushoverAPI
   >>> p = PushoverAPI('azGDORePK8gMaC0QOYAMyEEuzJnyUi')  # an instance of the PushoverAPI representing your application
   >>> p.send_message('uQiRzpo4DXghDmr9QzzfQu27cmVRsG', 'Your toast is finished.')  # send a message to a user

That's all you need to get started with sending Pushover notifications from your Python program.
The majority of Pushover's API endpoints are accessible via :code:`pushover_complete`.
Check out the `docs <http://pushover-complete.readthedocs.io/>`_ to learn more.

Installation
------------

Installation should be as easy as executing this command in your chosen terminal:

.. code-block:: sh

    $ pip install pushover_complete

:code:`pushover_complete` officially supports Python 2.7, 3.5, and 3.6.
Currently, Python 3.3 and 3.4 pass all tests and function properly as well, but this could change: these versions are not officially targeted by development.
Additionally, due to changes in Sphinx, the documentation cannot be built with Python 3.3.

As of version 1.1.0, support for Python 3.5 is deprecated. It will be removed in the next major version release.
This doesn't mean that Python 3.5 will stop working immediately, but I will no longer consider failing tests for that version to be critical.

Support for Python 2.x may be dropped in the future, but only in a major version update (e.g. 1.x.y → 2.x.y) and this change will be announced well in advance.

Contributing
------------

Contributions, large or small, from bug reports to pull requests and full-on forks, are highly encouraged.
Read the the `contributing page <http://pushover-complete.readthedocs.io/en/latest/contributing.html>`_ in the docs or :code:`CONTRIBUTING.rst` for more information on getting involved.

The full list of contributors is in :code:`AUTHORS.rst` or `on GitHub <https://github.com/scolby33/pushover_complete/contributors>`_.

Changelog
---------

Changes as of 6 April 2018

1.1.1 <6 April 2018>
^^^^^^^^^^^^^^^^^^^^

- HOTFIX for 1.1.0
- Fix Python versions badge in the documents index
- Add the Python 3.6 classifier in :code:`setup.py` so the right versions are shown on PyPI

1.1.0 <6 April 2018>
^^^^^^^^^^^^^^^^^^^^

- Add `image attachment support <https://pushover.net/api#attachments>`_ (Pulls `#5 <https://github.com/scolby33/pushover_complete/pull/5>`_ and `#9 <https://github.com/scolby33/pushover_complete/pull/9>`_)
- Officially add support for Python 3.6
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

License
-------

MIT. See the :code:`LICENSE.rst` file for more information.
