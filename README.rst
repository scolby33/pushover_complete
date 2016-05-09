pushover_complete
=================
A Python 3 package for interacting with *all* aspects of the Pushover API.

.. image:: https://travis-ci.org/scolby33/pushover_complete.svg?branch=master
    :target: https://travis-ci.org/scolby33/pushover_complete
    :alt: Build Status
.. image:: https://codecov.io/github/scolby33/pushover_complete/coverage.svg?branch=master
    :target: https://codecov.io/github/scolby33/pushover_complete?branch=master
    :alt: Test Coverage Status
.. image:: http://readthedocs.org/projects/pushover-complete/badge/?version=latest
    :target: http://pushover-complete.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

To learn more about Pushover and the Pushover API, please visit the Pushover Website, `<https://pushover.net>`_.

::

   >>> from pushover_complete import PushoverAPI
   >>> p = PushoverAPI('azGDORePK8gMaC0QOYAMyEEuzJnyUi')  # an instance of the PushoverAPI representing your application
   >>> p.send_message('uQiRzpo4DXghDmr9QzzfQu27cmVRsG', 'Your toast is finished.')  # send a message to a user

That's all you need to get started with sending Pushover notifications from your Python program.
The majority of Pushover's API endpoints are accessible via :code:`pushover_complete`.
Check out the `docs <http://pushover-complete.readthedocs.io/>`_ to learn more.

Installation
------------

Installation should be as easy as executing this command in your chosen terminal::

    $ pip install pushover_complete

Contributing
------------

Contributions, large or small, from bug reports to pull requests and full-on forks, are highly encouraged.
Read the the `contributing page <http://pushover-complete.readthedocs.io/en/latest/contributing.html>`_ in the docs or `CONTRIBUTING.rst <https://github.com/scolby33/pushover_complete/CONTRIBUTING.rst>`_ for more information on getting involved.

The full list of contributors is `here <https://github.com/scolby33/pushover_complete/AUTHORS.rst>`_.

License
-------

MIT. See the `LICENSE file <https://github.com/scolby33/pushover_complete/AUTHORS.rst>`_ for more information.
