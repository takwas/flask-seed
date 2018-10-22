#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask

from pytest import fixture

"""
test_flask_seed
----------------------------------

Tests for `flask_seed` module.
"""
from flask_seed import Seed


def test_command_line_interface(cli):
    runner = cli()

    result = runner.invoke(Seed)
    assert result.exit_code == 0

    help_result = runner.invoke(Seed, ['--help'])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output


def test_seed_dump(cli, seed, db, model):
    runner = cli()

    result = runner.invoke(Seed, ['dump'])
    assert "Dumping seed data from" in result.output
    assert result.exit_code == 0

    help_result = runner.invoke(Seed, ['dump', '--help'])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output


def test_seed_populate(cli, seed, db, model):
    runner = cli()

    m = model(test_data=42)
    db.session.add(m)
    db.session.commit()

    runner.invoke(Seed, ['dump'])  # create test data

    result = runner.invoke(Seed, ['populate'])
    assert "Building seed data from" in result.output
    assert "Loading {}...".format(model.__name__) in result.output
    assert result.exit_code == 0
    assert all(m.test_data == 42 for m in model.query.all())

    help_result = runner.invoke(Seed, ['populate', '--help'])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output
