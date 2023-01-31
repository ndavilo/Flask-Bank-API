from flask import Flask
import os
from src.auth import auth
from src.bank import bank
from src.dbmodels import db
basedir = os.path.abspath(os.path.dirname(__file__))

def create_app(test_config=None):
    app = Flask(
        __name__,
        instance_relative_config=True
        )
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'database.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False
        )
    else:
        app.config.from_mapping(test_config) 
        
    db.app=app
    db.init_app(app)
    app.register_blueprint(auth)
    app.register_blueprint(bank)
      
    return app