from sanic import Sanic
from blueprints import api
from database.init_db import create_tables


def create_app():
    app = Sanic(__name__)

    app.blueprint(api)

    create_tables()

    return app
