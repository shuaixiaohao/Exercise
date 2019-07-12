
import os

import redis
from flask import Flask
from flask_session import Session

from app.house_views import house_blueprint
from app.models import db
from app.user_views import user_blueprint
from app.order_views import order_blueprint
from utils.setting import BASE_DIR


se = Session()

def create_app():
    template_dir = os.path.join(BASE_DIR, 'templates')
    static_dir = os.path.join(BASE_DIR, 'static')
    app = Flask(__name__,
                template_folder=template_dir,
                static_folder=static_dir)

    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')
    app.register_blueprint(blueprint=house_blueprint, url_prefix='/house')
    app.register_blueprint(blueprint=order_blueprint, url_prefix='/order')

    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost:3306/aj"
    app.config['SQLALCHEMY_TRAKE_MODIFICATIONS'] = False

    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = redis.Redis('127.0.0.1', port=6379)

    db.init_app(app=app)
    se.init_app(app=app)
    return app
