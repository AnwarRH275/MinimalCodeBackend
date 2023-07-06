from flask import request, jsonify, make_response
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models.model import User
from werkzeug.security import generate_password_hash, check_password_hash
from models.exts import db
import random
import string


auth_ns = Namespace('auth', description='namespace for authentification')


# model (serializer)
signup_model = auth_ns.model(
    "SignUp",
    {
        "username": fields.String(),
        "email": fields.String(),
        "password": fields.String(),
        "tel": fields.String(),
        "nom": fields.String(),
        "prenom": fields.String(),
        "sexe": fields.String(),
        "date_naissance": fields.String(),

    }
)

# model (serializer)
login_model = auth_ns.model(
    "Login",
    {
        "username": fields.String(),
        "password": fields.String(),
    }
)


@auth_ns.route('/signup')
class SignUp(Resource):

    @auth_ns.expect(signup_model)
    def put(self):
        data = request.get_json()
        username_to_update = User.query.filter_by(
            username=data.get('username')).first()

        username_to_update.update(

            nom=data.get('nom'),
            tel=data.get('tel'),
            email=data.get('email'),
            sexe=data.get('sexe'),
            date_naissance=data.get('date_naissance')
        )

        return data

    @auth_ns.expect(signup_model)
    def post(self):
        data = request.get_json()
        username_find = User.query.filter_by(
            username=data.get('username')).first()
        # email_find = User.query.filter_by(email=data.get('email')).first()

        # print(email_find)
        if username_find is not None:
            return jsonify({"message": "User exist"})
        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password=generate_password_hash(data.get('password')),
            nom=data.get('nom'),
            prenom=data.get('prenom'),
            tel=data.get('tel'),

        )

        new_scores = Scores(

            username=data.get('username'),
            scores=0
        )
        letters_and_digits = string.ascii_uppercase + string.digits
        code = ''.join(random.choices(letters_and_digits, k=6))

        new_user.save()
        return make_response(jsonify({"message": "User created succes"}), 201)


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        username_find = User.query.filter_by(
            username=data.get('username')).first()
        if username_find is None:
            return jsonify({"message": "User not exist"})
        if check_password_hash(username_find.password, password):
            access_token = create_access_token(identity=username_find.username)
            refresh_token = create_refresh_token(
                identity=username_find.username)
            return jsonify({
                'acces_token': access_token,
                'refresh_token': refresh_token
            })
        else:
            return jsonify({"message": "password invalid"})


@auth_ns.route('/counter')
class counter(Resource):
    def get(self):
        total_count = User.query.count()
        return jsonify({'total_count': total_count})


@auth_ns.route('/delete/<string:username>', methods=['DELETE'])
class deleteUsers(Resource):
    def delete(self, username):
        user = User.query.filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': f'User {username} deleted.'})
        else:
            return jsonify({'message': f'User {username} not found.'})


@auth_ns.route('/refresh')
class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)

        return make_response(jsonify({"access_token": new_access_token}), 200)
