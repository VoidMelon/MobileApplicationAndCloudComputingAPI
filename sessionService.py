from flask import request, make_response, jsonify
from flask_restful import Resource

from db.sessiondb import insert_session_db


class SessionResource(Resource):
    def post(self, user_id):
        parameters = request.json
        msg, code = insert_session_db(parameters)
        return make_response(jsonify(msg), code)



