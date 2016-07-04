from .pushover_api import PushoverAPI
import click
import os
import sys
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

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


def read_configs(file_config=None):
    sys_config = os.path.join(_get_sys_dir(NAME), 'config.ini')
    usr_config = os.path.join(click.get_app_dir(NAME), 'config.ini')
    config = ConfigParser()
    config.read((sys_config, usr_config))
    if file_config:
        config.read_file(file_config)

    return config


@click.group(invoke_without_command=True)
@click.option('--token')
@click.option('--config', '-c', type=click.File())
@click.option('--preset', '-p', default='DEFAULT')
@click.version_option()
@click.pass_context
def cli(ctx, token, config, preset):
    ctx.obj = {'config': read_configs(config)}
    ctx.obj['api'] = PushoverAPI(token if token else ctx.obj['config'].get(preset, 'token'))
    click.echo(ctx.obj['api'])


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
    click.echo('MESSAGE: {}'.format(message))
    click.echo('USER: {}'.format(user))
    click.echo('DEVICE: {}'.format(device))
    click.echo('TITLE: {}'.format(title))
    click.echo('URL: {}'.format(url))
    click.echo('URL_TITLE: {}'.format(url_title))
    click.echo('PRIORITY: {}'.format(priority))
    click.echo('RETRY: {}'.format(retry))
    click.echo('EXPIRE: {}'.format(expire))
    click.echo('CALLBACK_URL: {}'.format(callback_url))
    click.echo('TIMESTAMP: {}'.format(timestamp))
    click.echo('SOUND: {}'.format(sound))
    click.echo('HTML: {}'.format(html))


@cli.command()
@click.pass_context
def sounds(ctx):
    pass


@cli.command()
@click.argument('user', required=False)
@click.option('--device')
@click.pass_context
def validate(ctx, user, device):
    click.echo('USER: {}'.format(user))
    click.echo('DEVICE: {}'.format(device))


@cli.command()
@click.argument('receipt', required=False)
@click.pass_context
def receipt(ctx, receipt):
    click.echo('RECEIPT: {}'.format(receipt))


@cli.command()
@click.argument('user', required=False)
@click.argument('subscription', required=False)
@click.option('--device')
@click.option('--sound')
@click.pass_context
def migrate(ctx, user, subscription, device, sound):
    click.echo('USER: {}'.format(user))
    click.echo('SUBSCRIPTION: {}'.format(subscription))
    click.echo('DEVICE: {}'.format(device))
    click.echo('SOUND: {}'.format(sound))


@cli.group(invoke_without_command=True)
@click.option('--group-key')
@click.pass_context
def group(ctx, group_key):
    click.echo('GROUP_KEY: {}'.format(group_key))


@group.command(name='add')
@click.argument('user', required=False)
@click.option('--device')
@click.option('--memo')
@click.pass_context
def group_add(ctx, user, device, memo):
    click.echo('USER: {}'.format(user))
    click.echo('DEVICE: {}'.format(device))
    click.echo('MEMO: {}'.format(memo))


@group.command(name='delete')
@click.argument('user', required=False)
@click.pass_context
def group_delete(ctx, user):
    click.echo('USER: {}'.format(user))


@group.command(name='disable')
@click.argument('user', required=False)
@click.pass_context
def group_disable(ctx, user):
    click.echo('USER: {}'.format(user))


@group.command(name='enable')
@click.argument('user', required=False)
@click.pass_context
def group_enable(ctx, user):
    click.echo('USER: {}'.format(user))


@group.command(name='rename')
@click.argument('new_name', required=False)
@click.pass_context
def group_rename(ctx, new_name):
    click.echo('NEW_NAME: {}'.format(new_name))


@cli.command()
@click.argument('user', required=False)
@click.pass_context
def assign(ctx, user):
    click.echo('USER: {}'.format(user))
