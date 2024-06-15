from flask import make_response, jsonify, request
from flask_restful import Resource

from db.environmentdb import get_all_environment_data_db, get_last_environment_data_db, insert_environment_data_db


class EnvironmentResource(Resource):
    def get(self, user_id, session_id):
        msg, code = get_last_environment_data_db(user_id, session_id)
        return make_response(jsonify(msg), code)

    def get(self, user_id, session_id, parameter):
        msg, code = get_all_environment_data_db(user_id, session_id)
        return make_response(jsonify(msg), code)

    def post(self, user_id, session_id):
        parameter = request.json
        msg, code = insert_environment_data_db(user_id, session_id, parameter)
        return make_response(jsonify(msg), code)


class EnvironmentDatasResource(Resource):
    def get(self, user_id, session_id):
        msg, code = get_all_environment_data_db(user_id, session_id)
        return make_response(jsonify(msg), code)