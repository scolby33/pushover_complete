.. pushover_complete documentation master file, created by
   sphinx-quickstart on Fri Apr 15 22:19:38 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. only:: prerelease

    .. warning:: This is the documentation for a development version of pushover_complete.

        .. only:: readthedocs

            `Documentation for the Most Recent Stable Version <http://pushover-complete.readthedocs.io/en/stable/>`_

Welcome to :mod:`pushover_complete`
===================================

:mod:`pushover_complete` is a Python package for interacting with *all* aspects of the `Pushover API <https://pushover.net/api>`_.

.. =========== =============== ================== ======================= ====================
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
    .. |stable_pyversions| image:: https://img.shields.io/badge/python-2.7%2C%203.5-blue.svg
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
    .. |develop_pyversions| image:: https://img.shields.io/badge/python-2.7%2C%203.5-blue.svg
        :alt: Development Supported Python Versions

To learn more about Pushover and the Pushover API, please visit the Pushover Website, `<https://pushover.net>`_.

::

   >>> from pushover_complete import PushoverAPI
   >>> p = PushoverAPI('azGDORePK8gMaC0QOYAMyEEuzJnyUi')  # an instance of the PushoverAPI representing your application
   >>> p.send_message('uQiRzpo4DXghDmr9QzzfQu27cmVRsG', 'Your toast is finished.')  # send a message to a user

That's all you need to get started with sending Pushover notifications from your Python program.
The majority of Pushover's API endpoints are accessible via :mod:`pushover_complete`.
Check out the :ref:`api` to see how.

On this page:

.. contents::
    :local:

Installation
------------

.. toctree::
    :maxdepth: 2
    :hidden:

    installation

Installation should be as easy as executing this command in your chosen terminal::

    $ pip install pushover_complete

The source code for this project is `hosted on Github <https://github.com/scolby33/pushover_complete>`_.
Downloading and installing from source goes like this::

    $ git clone https://github.com/scolby33/pushover_complete
    $ cd pushover_complete
    $ pip install .

If you intend to install in a virtual environment, activate it before running :code:`pip install`.

:mod:`pushover_complete` officially supports Python 2.7 and 3.5.
Currently, Python 3.3 and 3.4 pass all tests and function properly as well, but this could change: these versions are not officially targeted by development.
Support for Python 2.x may be dropped in the future, but only in a major version update (e.g. 1.x.y → 2.x.y) and this change will be announced well in advance.

See :ref:`installation` for further information about installing :mod:`pushover_complete` in all manner of ways.

Roadmap
-------

.. toctree::
    :maxdepth: 2
    :hidden:

    roadmap

:mod:`pushover_complete` emerged from my frustrating experience with a number of only partially-complete Pushover packages.
It is my goal to fully support all of Pushover's API endpoints in this package, beginning with the most essential ones and working from there.
The current status of progress towards this goal is tracked in the :ref:`roadmap <roadmap>`.

API Reference
-------------

Information about each function, class, and method is included here.

.. toctree::
    :maxdepth: 2

    api


Contributing
------------

.. toctree::
    :maxdepth: 2
    :hidden:

    contributing

:mod:`pushover_complete` is an open-source project and, so far, is mostly a one-person effort.
Any contributions are welcome, be they bug reports, pull requests, or otherwise.
Issues are tracked on `Github <https://github.com/scolby33/pushover_complete/issues>`_.

Check out :ref:`contributing` for more information on getting involved.

License Information
-------------------

.. toctree::
    :maxdepth: 2
    :hidden:

    license

:mod:`pushover_complete` is licensed under the MIT License, a permissive open-source license.

The full text of the license is available :ref:`here <license>` and in the root of the source code repository.

.. note:: This package is not written by or associated with Superblock, the creators of Pushover.
          The use of the name "Pushover" in the package name is authorized per Superblock's attribution rules.
          See the `logos section <https://pushover.net/press/logos>`_ of the Pushover website for more information.

Changelog
---------

.. toctree::
    :maxdepth: 2
    :hidden:

    changelog

:mod:`pushover_complete` adheres to the Semantic Versioning ("Semver") 2.0.0 versioning standard.
Details about this versioning scheme can be found on the `Semver website <http://semver.org/spec/v2.0.0.html>`_.
Versions postfixed with '-dev' are currently under development and those without a postfix are stable releases.

The current version of :mod:`pushover_complete` is |release|.

Full changelogs can be found on the :ref:`changelog` page.

.. toctree::
    :hidden:

    todo

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
