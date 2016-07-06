"""Tests for the CLI component of the package."""

from pushover_complete.pushover_cli import cli

from tests.fixtures import *


def test_test(cli_runner):
    result = cli_runner.invoke(cli)
    assert result
