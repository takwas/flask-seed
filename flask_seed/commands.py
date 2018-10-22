import os
import pickle

import click
from flask import current_app
from flask.cli import with_appcontext
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.ext.serializer import dumps, loads

from flask_seed.clo import register

__all__ = ['Seed', 'dump', 'populate']


@click.group()
def Seed():
    """populate or dump a database."""
    pass


cmd = Seed.command
opt = click.option


def get_models(model):
    """creates a model list of all submodels"""
    models = []
    if model.__subclasses__():
        for submodel in model.__subclasses__():
            models += get_models(submodel)
    else:
        models.append(model)

    return models


@register(cmd, opt, with_appcontext)
def dump(dumpfile=None):
    """Dumps database to `dumpfile`

    :param dumpfile: the path to the seed dump (defaults to ./seed.dmp)
    :type dumpfile: str
    """

    dumpfile = os.path.abspath(
        os.path.expanduser(dumpfile) or os.path.join(os.getcwd(), 'seed.pkl'))
    click.echo("Dumping seed data from {}".format(dumpfile))

    data = dict()
    current_db = current_app.extensions['flask_seed'].db
    for model in get_models(current_db.Model):
        click.echo("Saving {}...".format(model.__name__))
        query = current_db.session.query(model)
        data[model.__name__] = dumps(query.all())

    with open(dumpfile, 'wb') as file:
        pickle.dump(data, file)

    click.echo("Finished")


@register(cmd, opt, with_appcontext)
def populate(dumpfile=None):
    """Seeds database from `dumpfile`

    :param dumpfile: the path to the configuration data
    :type dumpfile: str
    """
    dumpfile = os.path.abspath(
        os.path.expanduser(dumpfile) or os.path.join(os.getcwd(), 'seed.pkl'))

    click.echo("Building seed data from {}".format(dumpfile))
    current_db = current_app.extensions['flask_seed'].db
    with open(dumpfile, 'rb') as file:
        data = pickle.load(file)

    for name, obj in data.items():
        data = loads(obj, current_db.metadata, current_db.session)
        click.echo("Loading {}...".format(name))
        for row in data:
            try:
                current_db.session.merge(row)
            except (IntegrityError, InvalidRequestError):
                current_db.session.rollback()

    click.echo("Finished")
