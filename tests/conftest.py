import json
import pytest

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from flask_seed import FlaskSeed

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    return app


@pytest.fixture
def cli(app):
    return app.test_cli_runner


@pytest.fixture
def db(app):
    _db = SQLAlchemy()
    _db.init_app(app)

    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def model(app, db):
    class _model(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        test_data = db.Column(db.Integer)

    with app.app_context():
        db.create_all()

    return _model


@pytest.fixture
def seed(app, db):
    _seed = FlaskSeed(app, db)
    return _seed
