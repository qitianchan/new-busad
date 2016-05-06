# -*- coding: utf-8 -*-
from flask import Flask, blueprints, url_for
from extentions import db, login_manager
from views import auth_blueprint, busad_blueprint
from models import User

def create_app():
    app = Flask(__name__)
    # app config
    app.config.from_object('config.DefaultConfig')

    _init_extention(app)
    _register_blueprint(app)
    with app.app_context():
        # create database
        db.create_all()
    return app


def _init_extention(app):
    """
    extention initial
    :param app:
    :return:
    """
    db.init_app(app)

    # login_manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth_blueprint.login'
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)


def _register_blueprint(app):
    """

    :param app:
    :return:
    """
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(busad_blueprint)


if __name__ == '__main__':
    app = create_app()
    app.run(port=8001)