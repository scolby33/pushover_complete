from collections import defaultdict
import copy
import os
from pprint import pprint
import sys
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

import click

from .pushover_api import PushoverAPI

NAME = 'Pushover Complete'


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


def _update_configs_from_args(ctx, args):
    args = copy.copy(args)
    try:
        args.pop('ctx')
    except KeyError:
        pass
    args = {k: v for k, v in args.items() if v}
    ctx.obj['config'].update(args)
    # pprint(ctx.obj['config'])


@click.group()
@click.option('--token')
@click.option('--config', '-c', type=click.File())
@click.option('--preset', '-p', default='DEFAULT')
@click.version_option()
@click.pass_context
def cli(ctx, token, config, preset):
    config = _read_configs(config)
    ctx.obj = {'config': defaultdict(lambda: None, config.items(preset))}
    if token:
        ctx.obj['config']['token'] = token
    ctx.obj['api'] = PushoverAPI(ctx.obj['config']['token'])


@cli.command()
@click.argument('message', required=False)
@click.option('--user')
@click.option('--device')
@click.option('--title')
@click.option('--url')
@click.option('--url-title')
@click.option('--priority')
@click.option('--retry')
@click.option('--expire')
@click.option('--callback-url')
@click.option('--timestamp')
@click.option('--sound')
@click.option('--html', is_flag=True)
@click.pass_context
def send(ctx, message, user, device, title, url, url_title, priority, retry, expire, callback_url, timestamp, sound, html):
    _update_configs_from_args(ctx, locals())


@cli.command()
@click.pass_context
def sounds(ctx):
    sounds_list = ctx.obj['api'].get_sounds()
    for identifier, name in sounds_list.items():
        print('{}: {}'.format(identifier, name))


@cli.command()
@click.argument('user', required=False)
@click.option('--device')
@click.pass_context
def validate(ctx, user, device):
    _update_configs_from_args(ctx, locals())


@cli.command()
@click.argument('receipt', required=False)
@click.pass_context
def receipt(ctx, receipt):
    _update_configs_from_args(ctx, locals())


@cli.command()
@click.argument('user', required=False)
@click.argument('subscription', required=False)
@click.option('--device')
@click.option('--sound')
@click.pass_context
def migrate(ctx, user, subscription, device, sound):
    _update_configs_from_args(ctx, locals())


@cli.group(invoke_without_command=True)
@click.option('--group-key')
@click.pass_context
def group(ctx, group_key):
    _update_configs_from_args(ctx, locals())


@group.command(name='add')
@click.argument('user', required=False)
@click.option('--device')
@click.option('--memo')
@click.pass_context
def group_add(ctx, user, device, memo):
    _update_configs_from_args(ctx, locals())


@group.command(name='delete')
@click.argument('user', required=False)
@click.pass_context
def group_delete(ctx, user):
    _update_configs_from_args(ctx, locals())


@group.command(name='disable')
@click.argument('user', required=False)
@click.pass_context
def group_disable(ctx, user):
    _update_configs_from_args(ctx, locals())


@group.command(name='enable')
@click.argument('user', required=False)
@click.pass_context
def group_enable(ctx, user):
    _update_configs_from_args(ctx, locals())


@group.command(name='rename')
@click.argument('new_name', required=False)
@click.pass_context
def group_rename(ctx, new_name):
    _update_configs_from_args(ctx, locals())


@cli.command()
@click.argument('user', required=False)
@click.pass_context
def assign(ctx, user):
    _update_configs_from_args(ctx, locals())
