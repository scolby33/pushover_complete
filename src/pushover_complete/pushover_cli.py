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
@click.pass_obj
def send(obj, message, **kwargs):
    pushover, cf = obj
    cf.update({k: v for k, v in kwargs.items() if v is not None})

    if 'user' not in cf:
        click.fail('missing USER')
    user = cf.pop('user')

    response = pushover.send_message(user, message, **cf)
    click.echo(response)
