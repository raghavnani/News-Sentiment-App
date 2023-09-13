import json
from flask import request, Response
from app.models.alchemy_encoder import AlchemyEncoder
from flask import Blueprint
from app.services.user_service import UserService

user_api = Blueprint('user_api', __name__)


@user_api.route('/api/createUser', methods=['POST'])
def create_user():
    email = request.json['email']
    user_name = request.json['user_name']
    password = request.json['password']
    results = UserService().create_user(email, user_name, password)
    result = json.dumps(results, cls=AlchemyEncoder)

    return Response(response=result, status=200, content_type="application/json")


@user_api.route('/api/updatePassword', methods=['POST'])
def update_password():
    id = request.json['id']
    password = request.json['password']
    results = UserService().update_user(id, password)
    result = json.dumps(results, cls=AlchemyEncoder)

    return Response(response=result, status=200, content_type="application/json")


@user_api.route('/api/getUserById', methods=['GET'])
def find_user_by_id():
    id = request.args.get('id')
    results = UserService().find_user_by_id(id)
    result = json.dumps(results, cls=AlchemyEncoder)

    return Response(response=result, status=200, content_type="application/json")


@user_api.route('/api/getAllUsers', methods=['GET'])
def find_all_user():
    results = UserService().find_all_users()
    result = json.dumps(results, cls=AlchemyEncoder)

    return Response(response=result, status=200, content_type="application/json")


@user_api.route('/api/getUserByEmail', methods=['POST'])
def find_user_by_email():
    email = request.json['email']
    password = request.json['password']

    results = UserService().find_user_by_email(email, password)
    result = json.dumps(results, cls=AlchemyEncoder)

    return Response(response=result, status=200, content_type="application/json")


@user_api.route('/api/saveNewsForUser', methods=['POST'])
def save_news_for_user():
    user_id = request.json['user_id']
    news_id = request.json['news_id']
    results = UserService().save_news_for_user(user_id, news_id)
    result = json.dumps(results, cls=AlchemyEncoder)

    return Response(response=result, status=200, content_type="application/json")

@user_api.route('/api/', methods=['GET'])
def hi():
    return 'hihihihi ==========================================================================='
