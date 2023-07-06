"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route("/signup", methods=["POST"])
def create_user():
    body = request.json
    new_user = User(
        username=body["username"],
        password=body["password"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@api.route("/login", methods=["POST"])
def handle_login():
    body = request.json
    username = body.get("username")
    password = body.get("password")

    # Perform authentication and validate user credentials
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        raise APIException("Invalid username or password", 401)

    # Authentication successful, return user information or token
    return jsonify(user.to_dict()), 200


@api.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list), 200
