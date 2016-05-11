.. only:: prerelease

    .. warning:: This is the documentation for a development version of pushover_complete.

        .. only:: readthedocs

            `Documentation for the Most Recent Stable Version <http://pushover-complete.readthedocs.io/en/stable/>`_

.. _installation:

Installation
============

There are many ways to install a Python package like :code:`pushover_complete`. Here many of those will be explained and the advantages of each will be identified.

If you are not yet familiar with virtual environments, stop reading this documentation and take a few moments to learn. Try some searches for "virtualenv," "virtualenvwrapper," and "pyvenv."
I promise that they will change your (Python) life.

Where to Get the Code
---------------------

From PyPI
^^^^^^^^^

Stable releases of :code:`pushover_complete` are located on PyPI, the `PYthon Package Index <https://pypi.python.org/pypi>`_.
Installation from here is easy and generally the preferred method::

    $ pip install pushover_complete


From GitHub
^^^^^^^^^^^

:code:`pip` is also able to install from remote repositories. Installation from this project's GitHub repo can get you the most recent release::

    $ pip install git+https://github.com/scolby33/pushover_complete@master#egg=pushover_complete-latest

This works because only release-ready code is pushed to the master branch.

To get the latest and greatest version of :code:`pushover_complete` from the develop branch, install like this instead::

    $ pip install git+https://github.com/scolby33/pushover_complete@develop#egg=pushover_complete-latestdev

In both of these cases, the :code:`#egg=pushover_complete-version` part of the URL is mostly arbitrary. The :code:`version` part is only useful for human readability and the :code:`pushover_complete` part is the project name used internally by :code:`pip`.

From a Local Copy
^^^^^^^^^^^^^^^^^

Finally, :code:`pip` can install from the local filesystem::

    $ cd /directory/containing/pushover_complete/setup.py
    $ pip install .

Installing like this lets you make changes to a copy of the project and use that custom version yourself!

Installing in Editable Mode
---------------------------

:code:`pip` has a :code:`--editable` (a.k.a. :code:`-e`) option that can be used to install from GitHub or a local copy in "editable" mode::

    $ pip install -e .

This, in short, installs the package as a symlink to the source files. That lets you edit the files in the :code:`src` folder and have those changes immediately available.
