__all__ = ['FlaskSeed']


class SeedConfig(object):
    def __init__(self, db=None):
        self.db = db


class FlaskSeed(object):

    def __init__(self, app=None, db=None):
        if app is not None and db is not None:
            self.init_app(app, db)

    @staticmethod
    def init_app(app, db):
        # can't force extensions to not exist in mocking
        if not hasattr(app, 'extensions'):
            app.extensions = {}  # pragma: no cover
        app.extensions['flask_seed'] = SeedConfig(db)
