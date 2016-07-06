"""Tests for the CLI component of the package."""

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
