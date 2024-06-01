from flask import request, make_response, jsonify
from flask_restful import Resource

from db.userdb import insert_user_db, delete_user_db, update_user_db, get_user_db


def validate_token(request):
    token = request.headers.get('Authorization')
    return True  # return the result of checking if the token is equal with the one in the config file


#inserire path per raggiungere l'api
#inserire interazione con db

class UserResource(Resource):
    def get(self, user_id):
        if not validate_token(request):
            return make_response(jsonify({'msg': 'Invalid Token'}), 401)
        msg, code = get_user_db(user_id)
        return make_response(jsonify(msg), code)

    def post(self):
        if not validate_token(request):
            return make_response(jsonify({'msg': 'Invalid Token'}, 401))
        parameters = request.json
        msg, code = insert_user_db(parameters)
        return make_response(jsonify(msg), code)

    def put(self, userid):
        if not validate_token(request):
            return make_response(jsonify({'msg': 'Invalid Token'}, 401))
        parameters = request.json
        msg, code = update_user_db(userid, parameters)
        return make_response(jsonify(msg), code)

    def delete(self, userid):
        if not validate_token(request):
            return make_response(jsonify({'msg': 'Invalid Token'}, 401))
        msg, code = delete_user_db(userid)
        return make_response(jsonify(msg), code)
