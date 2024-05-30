from flask import request, make_response, jsonify
from flask_restful import Resource
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.userdb import insert_user_db, delete_user_db


def validate_token(request):
    token = request.headers.get('Authorization')
    return True  # return the result of checking if the token is euqal with the one in the config file


#inserire path per raggiungere l'api
#inserire interazione con db

class UserResource(Resource):
    def get(self):
        if not validate_token(request):
            return make_response(jsonify({'message': 'Invalid Token'}, 401))
        parameters = request.json
        msg, code = insert_user_db(parameters)
        return make_response(jsonify(msg), code)

    def post(self):
        pass

    def put(self):
        pass

    def delete(self, userid):
        msg, code = delete_user_db(userid)
        return make_response(jsonify(msg), code)
