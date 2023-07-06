from flask import Flask
from flask_restx import Api, Resource
from config import DevConfig
from models.exts import db
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from services.auth.auth import auth_ns
from services.crud.manage import recipie_ns


app = Flask(__name__)


app.config.from_object(DevConfig)

CORS(app)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
JWTManager(app)

db.init_app(app)

migrate = Migrate(app, db)
api = Api(app, doc='/docs')

'''
    Create Migration repository
    $ flask db init 
    Apply Frist Migration
    $ flask db migrate  -m "add table"  
    Apply current revision db 'commit'
    $ flask db upgrade
'''


api.add_namespace(auth_ns)
api.add_namespace(recipie_ns)
# api.add_namespace(category_ns)
# api.add_namespace(match_ns)
# api.add_namespace(mesgrid_ns)
# api.add_namespace(scores_ns)
# api.add_namespace(coupons_ns)
# api.add_namespace(erreur_ns)
# api.add_namespace(affiliation_ns)
# api.add_namespace(uploadImage_ns)
# api.add_namespace(gagnant_ns)
# api.add_namespace(tokenNotification_ns)


if __name__ == '__main__':
    app.run(debug=True)
