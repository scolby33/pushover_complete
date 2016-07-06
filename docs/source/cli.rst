.. only:: prerelease

    .. warning:: This is the documentation for a development version of pushover_complete.

        .. only:: readthedocs

            `Documentation for the Most Recent Stable Version <http://pushover-complete.readthedocs.io/en/stable/>`_

.. _cli:

Command-Line Interface
======================

A command-line interface for interacting with the Pushover API using :mod:`pushover_complete` has been written
for convenience and as an example of how to use the package.

Using the CLI
-------------

The command-line tool is installed automatically alongside the package. It can be run by executing ``pushover`` from the shell.
If :mod:`pushover_complete` was installed inside a virtual environment, that environment must be activated to use the command.

If you want to be able to use the ``pushover`` command outside of a virtual environment but still want the isolation advantages provided by using one, check out the `pipsi project <https://github.com/mitsuhiko/pipsi>`_.

The command-line tool uses a command and option paradigm to allow access to all of the Pushover API.
There are a few examples below and extensive on-line documentation available by passing the ``--help`` option to the command or any of its subcommands.


Configuration Files
-------------------

The command-line tool has rich configuration capabilities based around a hierarchy of configuration files.

Configuration data is obtained from the following sources in the following order:

1. A system-wide configuration file

    - ``/etc/pushover-complete/config.ini`` on \*nix
    - ``/Library/Application Support/Pushover Complete/config.ini`` on OS X
    - ``%ALLUSERSPROFILE%\Pushover Complete\config.ini`` on Windows (``%ALLUSERSPROFILE%`` is generally ``C:\ProgramData\`` on Windows Vista and later or ``C:\Documents and Settings\All Users`` on XP)
2. A per-user configuration file

    - ``~/.config/pushover-complete/config.ini`` on \*nix
    - ``~/Library/Application Support/Pushover Complete/config.ini`` on OS X
    - ``%APPDATA%\Pushover Complete\config.ini`` on Windows (``%APPDATA%`` is generally ``C:\Users\<user>\AppData\Local`` on Windows Vista and later or ``C:\Documents and Settings\<user>\Application Data\`` on XP)
3. A configuration file passed with the ``--config/-c`` option
4. Values passed on the command line

The most specific configuration value is used. An option defined in multiple places is overridden by the most-recently read value.

Configuration files are specified in the traditional ``ini`` format and are parsed by Python's :mod:`configparser`.
An example configuration file is shown below::

    [DEFAULT]
    token=token_1
    user=user_1

    [reset-message]
    message=message_1
    user=user_2

    [alert]
    priority=1
    user=user_3

Let's say that the above file was located in the per-user configuration location. Then the invocation ``pushover send Message``
would be equivalent to ``pushover --token token_1 send --user user_1 Message``.

The invocation ``pushover -p alert send "New alert"`` would be equivalent to ``pushover --token token_1 send --user user_3 --priority 1 "New alert"``.
Notice how the ``token`` from the ``[DEFAULT]`` section is used since it has not been overridden by a ``token`` value in the ``[alert]`` section or on the command line.

They keys used in the configuration files have the same names as their corresponding command-line options, except hyphens are replaced with underscores (e.g. ``--group-key`` becomes ``group_key``).

Invalid keys in a configuration file will cause the command-line invocation to fail. The name of the offending key will be listed in the error message.
