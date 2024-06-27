from flask import request, make_response, jsonify
from flask_restful import Resource

from db.userdb import insert_user_db, delete_user_db, update_user_db, get_user_db


#inserire path per raggiungere l'api
#inserire interazione con db

class UserResource(Resource):
    def get(self, user_id):
        msg, code = get_user_db(user_id)
        return make_response(jsonify(msg), code)

    def post(self):
        parameters = request.json
        msg, code = insert_user_db(parameters)
        return make_response(jsonify(msg), code)

    def put(self, user_id):
        parameters = request.json
        msg, code = update_user_db(user_id, parameters)
        return make_response(jsonify(msg), code)

    def delete(self, user_id):
        msg, code = delete_user_db(user_id)
        return make_response(jsonify(msg), code)
