from flask import Flask
from flask_restx import Api, Resource
from flask_cors import CORS
from models.model import Recipie, User
from models.exts import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from services.auth.auth import auth_ns
from services.crud.manage import recipie_ns
from services.game.category import category_ns
from services.game.match import match_ns
from services.game.mesgrid import mesgrid_ns
from services.game.scores import scores_ns
from services.game.coupons import coupons_ns
from config import DevConfig


def create_app(config=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    JWTManager(app)
    db.init_app(app)
    
   

    # get Help db $ flask db
    '''
    Create Migration repository
    $ flask db init 
    Apply Frist Migration
    $ flask db migrate  -m "add table"
    Apply current revision db 'commit'
    $ flask db upgrade
    '''
    migrate = Migrate(app, db)
    api = Api(app, doc='/docs')

    api.add_namespace(auth_ns)
    api.add_namespace(recipie_ns)
    api.add_namespace(category_ns)
    api.add_namespace(match_ns)
    api.add_namespace(mesgrid_ns)
    api.add_namespace(scores_ns)
    api.add_namespace(coupons_ns)

    '''
    Acces to SHELL FLASK
    $ export FLASK_APP=main.py
    Acces to shell and Verifie link to db
    $ flask shell
    >>> db
    Locking classes
    >>> NameClass
    Create DB
    >>> db.create_all()
    '''

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "Recipie": Recipie,
            "User": User
        }

    return app
