from .pushover_api import PushoverAPI
import click
import os
import configparser

PUSHOVER_CONFIG = os.path.expanduser("~/.config/pushover_complete/config.ini")


@click.group()
@click.option('--config', '-c')
@click.option('--config-preset', '-p')
@click.option('--token', '-t')
@click.pass_context
def cli(ctx, config, config_preset, token):
    cf = dict()
    has_global_config = os.path.exists(PUSHOVER_CONFIG)

    if has_global_config or config:
        cfp = configparser.ConfigParser()
        cfp.read(PUSHOVER_CONFIG if has_global_config and config is None else config)
        cf = dict(cfp['DEFAULT'])
        if config_preset is not None:
            cf.update(cfp[config_preset])

        token = cf.pop('token')
        if token is None:
            ctx.fail("missing TOKEN")

    pushover = PushoverAPI(token)

    ctx.obj = pushover, cf


@cli.command()
@click.argument('message')
@click.option('--user')
@click.option('--device')
@click.option('--title')
@click.option('--url')
@click.option('--url-title')
@click.option('--priority')
@click.option('--retry', type=int)
@click.option('--expire', type=int)
@click.option('--callback-url')
@click.option('--timestamp', type=int)
@click.option('--sound')
@click.option('--html', type=int)
@click.pass_context
def send(ctx, message, **kwargs):
    pushover, cf = ctx.obj
    cf.update({k: v for k, v in kwargs.items() if v is not None})

    if 'user' not in cf:
        ctx.fail('missing USER')
    user = cf.pop('user')

    response = pushover.send_message(user, message, **cf)
    click.echo(response)


@cli.command()
@click.argument('user')
@click.argument('device')
@click.pass_obj
def validate(obj, user, device):
    pushover, cf = obj
    response = pushover.validate(user, device)
    click.echo(response)


@cli.command()
@click.argument('receipt')
@click.pass_obj
def check_receipt(obj, receipt):
    pushover, cf = obj
    response = pushover.check_receipt(receipt)
    click.echo(response)


@cli.command()
@click.argument('receipt')
@click.pass_obj
def cancel_receipt(obj, receipt):
    pushover, cf = obj
    response = pushover.cancel_receipt(receipt)
    click.echo(response)


@cli.command()
def migrate():
    pass


@cli.command()
@click.argument('user')
def assign(user):
    pass


@cli.group()
@click.option('group-key')
def group(group_key):
    pass


@group.command()
@click.argument('group')
@click.argument('user')
def add(group, user):
    pass


@group.command()
@click.argument('group')
@click.argument('user')
def delete(group, user):
    pass


@group.command()
@click.argument('group')
@click.argument('user')
def enable(group, user):
    pass


@group.command()
@click.argument('group')
@click.argument('user')
def disable(group, user):
    pass


@group.command()
@click.argument('group')
@click.argument('name')
def rename(group, name):
    pass
