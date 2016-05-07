.. _contributing:

Contributing
============

There are many ways to contribute to an open-source project, but the two most common are reporting bugs and issue and contributing code.

If you have a bug or issue to report, please visit the `issues page on Github <https://github.com/scolby33/pushover_complete/issues>`_ and open an issue there.

If you want to make a code contribution, read on for recommendations on how to set up your environment.

Setup
-----

Here's how to get set up to contribute to :code:`pushover_complete`.

#. Fork the :code:`pushover_complete` repository on `GitHub <https://github.com/scolby33/pushover_complete>`_
   (the fork button on the top right!)

#. If your change is small, you may be able to make it directly on GitHub via their online editing process.

   If your change is larger or you want to be able to run tests on your contribution, clone your forked repository locally::

    $ cd /your/dev/folder
    $ git clone https://www.github.com/your_username/pushover_complete

   This will download the contents of your forked repository to :code:`/your/dev/folder/pushover_complete`

#. If you're comfortable with a test-driven style of development, the only thing you need to install is `tox <http://tox.readthedocs.io/en/latest/>`_,
   either via the sometimes-temperamental but still useful `pipsi <https://github.com/mitsuhiko/pipsi>`_ (my choice), in a virtual environment,
   or just system-wide via pip::

    $ pipsi install tox
    # or
    $ pyvenv my-virtual-env
    $ source my-virtual-env/bin/activate
    $ pip install tox
    # or
    $ pip install tox

   With :code:`tox` installed, all tests, including checking the :code:`MANIFEST.in` file and code coverage can be performed
   just by executing::

    $ tox

   :code:`tox` handles the installation of all dependencies in virtual environments (under the :code:`.tox` folder) and
   the running of the tests.

   To develop like this, simply write your tests and your code and run :code:`tox` once in a while to check how you're doing.

   It is also possible to develop as usual by installing :code:`pushover_complete` in editable mode with pip (preferably in a virtual environment)::

    $ cd /your/dev/folder/pushover_complete
    $ cd pip install -e .

   Tests should still be run via :code:`tox`, but installing the package in this way gives you the flexibility to
   test things out in the REPL more easily.

Branches and Pull Requests
--------------------------

Code Style
----------
