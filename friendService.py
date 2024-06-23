from flask import make_response, jsonify, request
from flask_restful import Resource

from db.friend_db import get_friendlist, get_pendinglist, accept_friend_in_pending, decline_friend_request, \
    remove_friend_in_friendlist, get_user_by_username, add_friend_in_pending


class FriendResource(Resource):
    def get(self):
        user_id = request.json.get('user_id')
        msg, code = get_friendlist(user_id)
        return make_response(jsonify(msg), code)

    def delete(self):
        user_id = request.json.get('user_id')
        friend_id = request.json.get('friend_id')
        msg, code = remove_friend_in_friendlist(user_id, friend_id)
        return make_response(jsonify(msg), code)


class PendingResource(Resource):
    def get(self):
        user_id = request.json.get('user_id')
        msg, code = get_pendinglist(user_id)
        return make_response(jsonify(msg), code)

    def post(self):
        user_id = request.json.get('user_id')
        friend_in_pending_id = request.json.get('pending_id')
        msg, code = accept_friend_in_pending(user_id, friend_in_pending_id)
        return make_response(jsonify(msg), code)

    def delete(self):
        user_id = request.json.get('user_id')
        friend_id = request.json.get('friend_id')
        msg, code = decline_friend_request(user_id, friend_id)
        return make_response(jsonify(msg), code)


class SearchResource(Resource):
    def get(self):
        username = request.json.get('username')
        msg, code = get_user_by_username(username)
        return make_response(jsonify(msg), code)

    def post(self):
        user_id = request.json.get('user_id')
        sent_friend_request_id = request.json.get('sent_friend_request_id')
        msg, code = add_friend_in_pending(user_id, sent_friend_request_id)
        return make_response(jsonify(msg), code)

