"""Tests for the CLI component of the package."""

import re

try:
    from urllib.parse import urljoin, parse_qs
except ImportError:
    from urlparse import urljoin, parse_qs

import responses

from pushover_complete.pushover_cli import cli

from tests.constants import *
from tests.fixtures import *
from tests.responses_callbacks import *


def test_cli_outputs_help_with_no_arguments(cli_runner):
    result = cli_runner.invoke(cli)
    assert result.exit_code == 0
    assert result.output


@responses.activate
def test_cli_sends_simple_message(cli_runner):
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'messages.json'),
        callback=messages_callback,
        content_type='application/json'
    )

    result = cli_runner.invoke(cli, ['--token', TEST_TOKEN, 'send', '--user', TEST_USER, TEST_MESSAGE])
    assert result.exit_code == 0
    assert not result.output


@responses.activate
def test_cli_retrieves_sounds(cli_runner):
    responses.add_callback(
        responses.GET,
        urljoin(PUSHOVER_API_URL, 'sounds.json'),
        callback=sounds_callback,
        content_type='application/json'
    )

    result = cli_runner.invoke(cli, ['--token', TEST_TOKEN, 'sounds'])
    assert result.exit_code == 0
    assert sorted(result.output.splitlines()) == sorted('{}: {}'.format(identifier, name) for identifier, name in SOUNDS.items())


@responses.activate
def test_cli_validates_user(cli_runner):
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'users/validate.json'),
        callback=validate_callback,
        content_type='application/json'
    )

    result = cli_runner.invoke(cli, ['--token', TEST_TOKEN, 'validate', TEST_USER])
    assert result.exit_code == 0
    assert not result.output


@responses.activate
def test_cli_validates_group(cli_runner):
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'users/validate.json'),
        callback=validate_callback,
        content_type='application/json'
    )

    result = cli_runner.invoke(cli, ['--token', TEST_TOKEN, 'validate', TEST_GROUP])
    assert result.exit_code == 0
    assert not result.output


@responses.activate
def test_cli_gets_receipt(cli_runner):
    url_re = re.compile('https://api\.pushover\.net/1/receipts/r[a-zA-Z0-9]*\.json')
    responses.add_callback(
        responses.GET,
        url_re,
        callback=receipt_callback,
        content_type='application/json'
    )

    result = cli_runner.invoke(cli, ['--token', TEST_TOKEN, 'receipt', '--receipt', TEST_RECEIPT_ID])
    assert result.exit_code == 0
    assert result.output


@responses.activate
def test_cli_cancel_receipt(cli_runner):
    url_re = re.compile('https://api\.pushover\.net/1/receipts/r[a-zA-Z0-9]*/cancel\.json')
    responses.add_callback(
        responses.POST,
        url_re,
        callback=receipt_cancel_callback,
        content_type='application/json'
    )

    result = cli_runner.invoke(cli, ['--token', TEST_TOKEN, 'receipt', '--receipt', TEST_RECEIPT_ID, 'cancel'])
    assert result.exit_code == 0
    assert not result.output


@responses.activate
def test_cli_migrate(cli_runner):
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'subscriptions/migrate.json'),
        callback=subscription_migrate_callback,
        content_type='application/json'
    )

    result = cli_runner.invoke(cli, ['--token', TEST_TOKEN, 'migrate', '--subscription-code', TEST_SUBSCRIPTION_CODE, TEST_USER])
    assert result.exit_code == 0
    assert result.output.strip() == TEST_SUBSCRIBED_USER_KEY


@responses.activate
def test_cli_group(cli_runner):
    url_re = re.compile('https://api\.pushover\.net/1/groups/g[a-zA-Z0-9]*\.json')
    responses.add_callback(
        responses.GET,
        url_re,
        callback=groups_callback,
        content_type='application/json'
    )

    result = cli_runner.invoke(cli, ['--token', TEST_TOKEN, 'group', '--group-key', TEST_GROUP])
    parsed_result = json.loads(result.output)
    assert result.exit_code == 0
    assert parsed_result['name'] == 'Test Group'
    assert len(parsed_result['users']) == 2


@responses.activate
def test_cli_add_to_group(cli_runner):
    url_re = re.compile('https://api\.pushover\.net/1/groups/g[a-zA-Z0-9]*/add_user\.json')
    responses.add_callback(
        responses.POST,
        url_re,
        callback=groups_add_user_callback,
        content_type='application/json'
    )

    result = cli_runner.invoke(cli, ['--token', TEST_TOKEN, 'group', '--group-key', TEST_GROUP, 'add', TEST_USER])

    assert result.exit_code == 0
    assert not result.output
