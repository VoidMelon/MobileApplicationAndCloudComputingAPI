from flask import request, make_response, jsonify
from flask_restful import Resource

from db.sessiondb import insert_session_db, delete_session_db, get_all_sessions_db, get_session_db


class SessionResource(Resource):
    def get(self, user_id):
        msg, code = get_all_sessions_db(user_id)
        return make_response(jsonify(msg), code)

    def get(self, user_id, session_id):
        msg, code = get_session_db()
        return make_response(jsonify(msg), code)

    def post(self, user_id):
        parameters = request.json
        msg, code = insert_session_db(user_id, parameters)
        return make_response(jsonify(msg), code)

    def delete(self, user_id, session_id):
        msg, code = delete_session_db(user_id, session_id)
        return make_response(jsonify(msg), code)
