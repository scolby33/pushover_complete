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

.. versionadded:: 1.1.0 Additionally, the `image attachment functionality <https://pushover.net/api#attachments>`_ added to Pushover in January 2018 `with version 3.0 of the Pushover apps <https://updates.pushover.net/post/170043375237/pushing-images-with-pushover-30>`_ is now supported.

A command line interface is in the works to allow use directly from your shell.

The Pushover Open Client API may be implemented for a future release.
