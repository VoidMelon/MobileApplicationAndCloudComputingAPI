from flask import make_response, jsonify
from flask_restful import Resource


class FriendResource(Resource):
    def get(self, user_id):
        msg, code = get_friendlist(user_id)
        return make_response(jsonify(msg), code)


class PendingResource(Resource):
    def get(self, user_id):
        msg, code = get_pendinglist(user_id)
        return make_response(jsonify(msg), code)