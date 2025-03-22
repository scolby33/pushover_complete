.. only:: prerelease

    .. warning:: This is the documentation for a development version of pushover_complete.

        .. only:: readthedocs

            `Documentation for the Most Recent Stable Version <http://pushover-complete.readthedocs.io/en/stable/>`_

.. _contributing:

Contributing
============

There are many ways to contribute to an open-source project, but the two most common are reporting bugs and issues and
contributing code.

If you have a bug or issue to report, please visit the
`issues page on Github <https://github.com/scolby33/pushover_complete/issues>`_ and open an issue there.

If you want to make a code contribution, read on for recommendations on how to set up your environment.

.. note:: Remember to add yourself to :code:`AUTHORS.rst` if you make a code contribution!

Setup
-----

Here's how to get set up to contribute to :code:`pushover_complete`.

#. Fork the :code:`pushover_complete` repository on `GitHub <https://github.com/scolby33/pushover_complete>`_
   (the fork button on the top right!)

#. If your change is small, you may be able to make it directly on GitHub via their online editing process.

   If your change is larger or you want to be able to run tests on your contribution, clone your forked repository
   locally::

    $ cd ~/src
    $ git clone https://github.com/your_username/pushover_complete

   This will download the contents of your forked repository to :code:`~/src/pushover_complete`

#. If you're comfortable with a test-driven style of development, the only thing you need to install is
   `uv <https://docs.astral.sh/uv/>`_. You can then run the tests using `tox <http://tox.readthedocs.io/en/latest/>`_
   without having to worry too much about other installation steps::

    $ uv tool run --with tox-uv tox

   :code:`tox` handles the installation of all dependencies in virtual environments (under the :code:`.tox` folder) and
   the running of the tests.

   To develop like this, simply write your tests and your code and run :code:`tox` as above once in a while to check how
   you're doing.

   It is also possible to develop as usual by installing :code:`pushover_complete` in editable mode with pip
   (preferably in a virtual environment)::

    $ cd /your/dev/folder/pushover_complete
    $ cd pip install -e .

   Tests should still be run via :code:`tox`, but installing the package in this way gives you the flexibility to test
   things out in the REPL more easily.

Branches
--------

Development of :code:`pushover_complete` follows a common but ad-hoc style of branching. Development takes place on the
:code:`develop` branch with individual features being developed on feature branches off of develop. Releases are made
by merging the :code:`develop` branch to the :code:`master` branch, creating a tag, and creating a GitHub release from
there. GitHub Actions handle building and publishing the distributions to PyPI.

This might seem a bit complicated, but in general you won't have to worry about it as a contributor.
The long and short of this system for you is:

- make a new branch off of develop before starting work on your contribution
  (:code:`git checkout -b feature/descriptive-feature-name develop`)
- when pushing changes to your repository, push the right branch!
  (:code:`git push origin feature/descriptive-feature-name`)

The maintainers will take care of any other issues relating to this.

Pull Requests
-------------

Once you've got your feature or bugfix finished (or if it's in a partially complete state but you want to publish it
for comment), push it to your fork of the repository and open a pull request against the develop branch on GitHub.

Make a descriptive comment about your pull request, perhaps referencing the issue it is meant to fix (something along
the lines of "fixes issue #10" will cause GitHub to automatically link to that issue).
The maintainers will review your pull request and perhaps make comments about it, request changes, or may pull it in to
the develop branch!
If you need to make changes to your pull request, simply push more commits to the feature branch in your fork to GitHub
and they will automatically be added to the pull.
You do not need to close and reissue your pull request to make changes!

If you spend a while working on your changes, further commits may be made to the main :code:`pushover_complete`
repository (called "upstream") before you can make your pull request.
In keep your fork up to date with upstream by pulling the changes--if your fork has diverged too much, it becomes
difficult to properly merge pull requests without conflicts.

To pull in upstream changes::

    $ git remote add upstream https://github.com/scolby33/pushover_complete
    $ git fetch upstream develop

Check the log to make sure the upstream changes don't affect your work too much::

    $ git log upstream/develop

Then merge in the new changes::

    $ git merge upstream/develop

More information about this whole fork-pull-merge process can be found
`here on Github's website <https://help.github.com/articles/fork-a-repo/>`_.

Code Style
----------

To make sure your contribution is useful to the overall :code:`pushover_complete` project, you should follow a few
conventions.

Run the Tests
^^^^^^^^^^^^^

Make sure your modifications still pass all tests before submitting a pull requests::

    $ uv tool run --with tox-uv tox

Changes that break the package are mostly useless.

Add New Tests
^^^^^^^^^^^^^

If you add functionality, you must add tests for it! Untested code is antithetical to reliability.
Pull requests that reduce code coverage will likely be rejected.
You can check your coverage in the output from :code:`tox`. Lines and files that lack test coverage will be noted there
too!

Check out the tests (files that start with :code:`test_` under :code:`src/tests`) to see how previous tests have been
written and match your new tests to this style.
Tests are performed with :code:`pytest`.

Try and keep your tests simple--tests shouldn't need tests for themselves! Some verbosity in tests isn't the end of the
world if it helps to maintain clarity.

Keep Code Changes and Whitespace Cleanup Separate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is pretty self-explanatory. Code changes and whitespace cleanup should not be mixed--keep them in separate pull
requests.

Keep Pull Requests Small
^^^^^^^^^^^^^^^^^^^^^^^^

Generally, pull requests should be targeted towards one issue. If you find yourself modifying large swathes of code
spanning multiple fixes, thing about splitting your pull request into two (or more!) smaller ones.
Large pull requests will likely be rejected.

Follow PEP-8 (ish) and the Zen of Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you haven't before, check out the Zen of Python (:code:`python -c 'import this'`) and attempt to keep your code in
line with its philosophy.
Simple is better than complex!

Keep best practices for formatting Python code in mind when writing your contribution.
`PEP-8 <https://www.python.org/dev/peps/pep-0008/>`_ is generally followed in this project, but not pedantically. Line
lengths, for example, are often allowed to creep up if it seems reasonable.
If you haven't seen Raymond Hettinger's `Beyond PEP 8 <https://www.youtube.com/watch?v=wf-BqAjZb8M>`_ presentation, I
urge you to go watch it.
Unthinking adherence to the "rules" of PEP-8 is not demanded nor is it the best way to write good, Pythonic code.

Making a Release
----------------

The steps for making a release of :code:`pushover_complete` are:

#. Create a release branch off of :code:`develop`::

     $ git switch -c release/$(uv tool run bump-my-version show --increment release new_version) develop

#. Bump the version specifiers::

     $ uv tool run bump-my-version release

#. Update the changelogs and commit them

   #. Update the changelog in :code:`docs/source/changelog.rst`, including the last updated date
   #. Update the changelog in :code:`README.rst` to match the changelog in the docs

#. Check that any new intersphinx links have corresponding inventory locations in :code:`docs/source/conf.py`. Run

    ::

    $ egrep -rIn --exclude-dir=.eggs --exclude-dir=.tox --exclude-dir=build ':\S+:' .

   and check for instances of :code:`:meth:`, :code:`:class:`, etc. that are from sources not already included in
   :code:`intersphinx_mapping` in :code:`conf.py`. (There will be a lot of lines, but with :code:`grep` coloring turned
   on, it's not that hard to skim through relatively quickly.)

#. Open a PR for the release branch into the develop branch and check that all tests pass before merging it

#. `Open a PR <https://github.com/scolby33/pushover_complete/compare/master...develop>`_ for the develop branch into
   master and check that all tests pass before merging it

#. Create a GitHub release and corresponding tag from the master branch. Make sure to mark it as a pre-release or not
   as appropriate.

#. Add changelog notes to the release on GitHub

#. Check that the release build has completed successfully and the distributions have been published to PyPI. (You might
   want to try a test install from PyPI at this point.)

#. Bump the version to the next dev version::

    $ bumpversion patch

