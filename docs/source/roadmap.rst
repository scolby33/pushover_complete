.. only:: prerelease

    .. warning:: This is the documentation for a development version of pushover_complete.

        .. only:: readthedocs

            `Documentation for the Most Recent Stable Version <http://pushover-complete.readthedocs.io/en/stable/>`_

.. _roadmap:

Roadmap
=======

The following Pushover API endpoints are fully implemented:
    - /messages.json
    - /sounds.json
    - /users/validate.json
    - /receipts/{receipt}.json
    - /receipts/{receipt}/cancel.json
    - /subscriptions/migrate.json   - /groups/{group_key}.json
    - /groups/{group_key}/add_user.json
    - /groups/{group_key}/delete_user.json
    - /groups/{group_key}/disable_user.json
    - /groups/{group_key}/enable_user.json
    - /groups/{group_key}/rename.json
    - /licenses/assign.json

This constitutes all of the API endpoints available for entities acting as Pushover applications.

A command line interface is in the works to allow use directly from the shell.

The Pushover Open Client API may be implemented for a future release.
