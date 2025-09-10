.. only:: prerelease

    .. warning:: This is the documentation for a development version of pushover_complete.

        .. only:: readthedocs

            `Documentation for the Most Recent Stable Version <http://pushover-complete.readthedocs.io/en/stable/>`_

.. _api:

API Reference
=============

.. module:: pushover_complete

This part of the documentation covers all of the interfaces exposed by :mod:`pushover_complete`.

The PushoverAPI Class
---------------------
This class is your gateway to interacting with the Pushover API.
Each instance is initialized with a Pushover application token and makes API calls on behalf of that application.

Main Interface
^^^^^^^^^^^^^^

The methods represent most of the useful functions of :class:`PushoverAPI`.

.. autoclass:: PushoverAPI
    :members:


"Private" Methods
^^^^^^^^^^^^^^^^^

These methods, although "private" and used internally by other :class:`PushoverAPI` methods could be useful in some
circumstances, particularly when many requests are to be made at one time.

.. class:: PushoverAPI
   :no-index:

    .. automethod:: _send_message
    .. automethod:: _migrate_to_subscription
    .. automethod:: _generic_get
    .. automethod:: _generic_post


Helper Types
^^^^^^^^^^^^

.. module:: pushover_complete.apibase
.. autodata:: ResponseStatusSuccess
.. autodata:: ResponseStatusError
.. autotypeddict:: SuccessResponse
.. autotypeddict:: ErrorResponse


.. module:: pushover_complete.message_api
.. autotypeddict:: MessageRequest
.. autotypeddict:: MultiMessageRequest
.. autotypeddict:: MessageResponse
.. autodata:: SoundName
.. autodata:: SoundDescription
.. autodata:: SoundsResponse
.. autotypeddict:: LimitsResponse

.. module:: pushover_complete.user_group_validation_api
.. autotypeddict:: UserValidationResponse

.. module:: pushover_complete.receipt_and_callback_api
.. autodata:: AcknowledgeStatusAcknowledged
.. autodata:: AcknowledgeStatusUnacknowledged
.. autodata:: AcknowledgeStatus
.. autodata:: ExpiredStatusExpired
.. autodata:: ExpiredStatusUnexpired
.. autodata:: ExpiredStatus
.. autodata:: CallbackStatusCalledBack
.. autodata:: CallbackStatusNotCalledBack
.. autodata:: CallbackStatus
.. autotypeddict:: ReceiptResponse

.. module:: pushover_complete.subscription_api
.. autotypeddict:: UserSubscriptionRequest
.. autotypeddict:: MultiUserSubscriptionRequest
.. autotypeddict:: SubscriptionResponse

.. module:: pushover_complete.groups_api
.. autotypeddict:: GroupCreateResponse
.. autotypeddict:: GroupUser
.. autotypeddict:: GroupInfoResponse
.. autotypeddict:: GroupListInfo
.. autotypeddict:: GroupsListResponse

.. module:: pushover_complete.licensing_api
.. autotypeddict:: LicenseResponse


Exceptions and Errors
---------------------

.. module:: pushover_complete
   :no-index:

.. autoexception:: PushoverCompleteError
.. autoexception:: BadAPIRequestError
