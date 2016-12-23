from collections import defaultdict
import copy
import json
import os
from pprint import pprint
import sys
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

import click

from .pushover_api import PushoverAPI, BadAPIRequestError

NAME = 'Pushover Complete'
MISSING_ARG = 'Required input missing: {}'


def _get_sys_dir(app_name, force_posix=False):
    if click._compat.WIN:  # C:\ProgramData\{app_name} or C:\Documents and Settings\All Users\{app_name}
        folder = os.environ.get('ALLUSERSPROFILE')
        return os.path.join(folder, app_name)
    if force_posix:  # /etc/{app_name}
        return os.path.join('/etc', click.utils._posixify(app_name))
    if sys.platform == 'darwin':  # /Library/Application Support/{app_name}
        return os.path.join('/Library/Application Support', app_name)
    return os.path.join('/etc', click.utils._posixify(app_name))  # /etc/{app_name}


def _read_configs(file_config=None):
    sys_config = os.path.join(_get_sys_dir(NAME), 'config.ini')
    usr_config = os.path.join(click.get_app_dir(NAME), 'config.ini')
    config = ConfigParser()
    config.read((sys_config, usr_config))
    if file_config:
        config.read_file(file_config)

    return config


def _update_configs_from_args(ctx, args, keys_to_remove=None):
    args = copy.copy(args)
    try:
        args.pop('ctx')
    except KeyError:
        pass
    args = {k: v for k, v in args.items() if v}
    ctx.obj['config'].update(args)
    if keys_to_remove:
        for key in keys_to_remove:
            ctx.obj['config'].pop(key)
    # pprint(ctx.obj['config'])


@click.group()
@click.option('--token', metavar='TOKEN', help='A Pushover application token')
@click.option('--config', '-c', type=click.File(), help='A configuration file to override system- and user-level configuration files')
@click.option('--preset', '-p', default='DEFAULT', help='A configuration preset to apply')
@click.version_option()
@click.pass_context
def cli(ctx, token, config, preset):
    """Interact with the Pushover API via command line.

    Brought to you by the `pushover_complete` Python package.
    """
    config = _read_configs(config)
    ctx.obj = {'config': defaultdict(lambda: None, config.items(preset))}
    if token:
        ctx.obj['config']['token'] = token
    ctx.obj['api'] = PushoverAPI(ctx.obj['config']['token'])


@cli.command()
@click.argument('message', required=False)
@click.option('--user', metavar='TOKEN', help='A Pushover user token representing the user or group to whom the message will be sent')
@click.option('--device', help='A comma-separated string representing the device(s) to which the message will be sent')
@click.option('--title', help='The title of the message')
@click.option('--url', metavar='URL', help='A URL to be included with the message')
@click.option('--url-title', help='The link text to be displayed for the URL. If omitted, the URL itself is displayed.')
@click.option('--priority', metavar='INT', help='An integer representing the priority of the message, from -2 (least important) to 2 (emergency). Default is 0.')
@click.option('--retry', metavar='INT', help='How often the Pushover server will re-send an emergency-priority message in seconds. Required with priority 2 messages.')
@click.option('--expire', metavar='INT', help='How long an emergency-priority message will be re-sent for in seconds')
@click.option('--callback-url', metavar='URL', help='A url to be visited by the Pushover servers upon acknowledgement of an emergency-priority message')
@click.option('--timestamp', metavar='INT', help="A Unix timestamp of the message's date and time to be displayed instead of the time the message is received by the Pushover servers")
@click.option('--sound', help="A string representing the sound to be played with the message instead of the user's default. Available sounds can be retreived using the `sounds` command.")
@click.option('--html', is_flag=True, help='A flag representing if HTML formatting will be enabled for the message text')
@click.pass_context
def send(ctx, message, user, device, title, url, url_title, priority, retry, expire, callback_url, timestamp, sound, html):
    """Send [MESSAGE] via the Pushover API."""
    _update_configs_from_args(ctx, locals(), ('token',))
    try:
        ctx.obj['api'].send_message(**ctx.obj['config'])
    except TypeError as e:
        ctx.fail(MISSING_ARG.format(e.args[0].split(':')[1].strip()))
    except BadAPIRequestError as e:
        ctx.exit(e.args[0].split(':')[-1].strip())


@cli.command()
@click.pass_context
def sounds(ctx):
    """Get the current list of supported sounds from the Pushover servers."""
    try:
        sounds_list = ctx.obj['api'].get_sounds()
    except BadAPIRequestError as e:
        ctx.exit(e.args[0].split(':')[-1].strip())
    for identifier, name in sounds_list.items():
        print('{}: {}'.format(identifier, name))


@cli.command()
@click.argument('user', required=False)
@click.option('--device', help='A string representing a device name to validate')
@click.pass_context
def validate(ctx, user, device):
    """Validate a user or group token or a user device."""
    _update_configs_from_args(ctx, locals(), ('token',))
    try:
        ctx.obj['api'].validate(**ctx.obj['config'])
    except TypeError as e:
        ctx.fail(MISSING_ARG.format(e.args[0].split(':')[1].strip()))
    except BadAPIRequestError as e:
        ctx.exit(e.args[0].split(':')[-1].strip())


@cli.group(invoke_without_command=True)
@click.option('--receipt', metavar='TOKEN', help='The receipt id')
@click.pass_context
def receipt(ctx, receipt):
    """Check a receipt issued after sending an emergency-priority message. Prints the JSON-formatted result of the API call."""
    _update_configs_from_args(ctx, locals(), ('token',))
    if not ctx.invoked_subcommand:
        try:
            receipt_details = ctx.obj['api'].check_receipt(**ctx.obj['config'])
        except TypeError as e:
            ctx.fail(MISSING_ARG.format(e.args[0].split(':')[1].strip()))
        except BadAPIRequestError as e:
            ctx.exit(e.args[0].split(':')[-1].strip())

        print(json.dumps(receipt_details, indent=2, sort_keys=True))


@receipt.command(name='cancel')
@click.pass_context
def receipt_cancel(ctx):
    """Cancel a receipt (and thus further re-sends of the message)."""
    _update_configs_from_args(ctx, locals())
    try:
        ctx.obj['api'].cancel_receipt(**ctx.obj['config'])
    except TypeError as e:
        ctx.fail(MISSING_ARG.format(e.args[0].split(':')[1].strip()))
    except BadAPIRequestError as e:
        ctx.exit(e.args[0].split(':')[-1].strip())


@cli.command()
@click.argument('user', required=False)
@click.option('--subscription-code', metavar='TOKEN', help='The subscription code to migrate the user to')
@click.option('--device', help="The user's device that the subscription will be limited to")
@click.option('--sound', help="The user's preferred sound")
@click.pass_context
def migrate(ctx, user, subscription_code, device, sound):
    """Migrate [USER] to a subscription key."""
    _update_configs_from_args(ctx, locals(), ('token',))
    try:
        ctx.obj['api'].migrate_to_subscription(**ctx.obj['config'])
    except TypeError as e:
        ctx.fail(MISSING_ARG.format(e.args[0].split(':')[1].strip()))
    except BadAPIRequestError as e:
        ctx.exit(e.args[0].split(':')[-1].strip())


@cli.group(invoke_without_command=True)
@click.option('--group-key', metavar='TOKEN', help='A Pushover group key')
@click.pass_context
def group(ctx, group_key):
    """Retrieve information about a delivery group."""
    _update_configs_from_args(ctx, locals(), ('token',))
    if not ctx.invoked_subcommand:
        try:
            pprint(ctx.obj['api'].group_info(**ctx.obj['config']))
        except TypeError as e:
            ctx.fail(MISSING_ARG.format(e.args[0].split(':')[1].strip()))
        except BadAPIRequestError as e:
            ctx.exit(e.args[0].split(':')[-1].strip())


@group.command(name='add')
@click.argument('user', required=False)
@click.option('--device', help='The user key to be added to the group')
@click.option('--memo', help='A string representing the device name to add to the group')
@click.pass_context
def group_add(ctx, user, device, memo):
    """Add [USER] to a group."""
    _update_configs_from_args(ctx, locals())
    try:
        ctx.obj['api'].group_add_user(**ctx.obj['config'])
    except TypeError as e:
        ctx.fail(MISSING_ARG.format(e.args[0].split(':')[1].strip()))
    except BadAPIRequestError as e:
        ctx.exit(e.args[0].split(':')[-1].strip())


@group.command(name='delete')
@click.argument('user', required=False)
@click.pass_context
def group_delete(ctx, user):
    """Remove [USER] from a group."""
    _update_configs_from_args(ctx, locals())
    try:
        ctx.obj['api'].group_delete_user(**ctx.obj['config'])
    except TypeError as e:
        ctx.fail(MISSING_ARG.format(e.args[0].split(':')[1].strip()))
    except BadAPIRequestError as e:
        ctx.exit(e.args[0].split(':')[-1].strip())


@group.command(name='disable')
@click.argument('user', required=False)
@click.pass_context
def group_disable(ctx, user):
    """Temporarily disable [USER] in a group."""
    _update_configs_from_args(ctx, locals())
    try:
        ctx.obj['api'].group_disable_user(**ctx.obj['config'])
    except TypeError as e:
        ctx.fail(MISSING_ARG.format(e.args[0].split(':')[1].strip()))
    except BadAPIRequestError as e:
        ctx.exit(e.args[0].split(':')[-1].strip())


@group.command(name='enable')
@click.argument('user', required=False)
@click.pass_context
def group_enable(ctx, user):
    """Re-enable [USER] in a group."""
    _update_configs_from_args(ctx, locals())
    try:
        ctx.obj['api'].group_enable_user(**ctx.obj['config'])
    except TypeError as e:
        ctx.fail(MISSING_ARG.format(e.args[0].split(':')[1].strip()))
    except BadAPIRequestError as e:
        ctx.exit(e.args[0].split(':')[-1].strip())


@group.command(name='rename')
@click.argument('new_name', required=False)
@click.pass_context
def group_rename(ctx, new_name):
    """Change the name of a group to [NEW_NAME]."""
    _update_configs_from_args(ctx, locals())
    try:
        ctx.obj['api'].group_rename(**ctx.obj['config'])
    except TypeError as e:
        ctx.fail(MISSING_ARG.format(e.args[0].split(':')[1].strip()))
    except BadAPIRequestError as e:
        ctx.exit(e.args[0].split(':')[-1].strip())


@cli.command()
@click.argument('user', required=False)
@click.pass_context
def assign(ctx, user):
    """Assign a Pushover license to [USER]."""
    _update_configs_from_args(ctx, locals(), ('token',))
    try:
        ctx.obj['api'].assign_license(**ctx.obj['config'])
    except TypeError as e:
        ctx.fail(MISSING_ARG.format(e.args[0].split(':')[1].strip()))
    except BadAPIRequestError as e:
        ctx.exit(e.args[0].split(':')[-1].strip())
