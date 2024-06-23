from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker

from model.models import User, UserSchema, friendship

# engine = create_engine("postgresql://melon:MobileCloud!@localhost/mobile-project")
engine = create_engine("postgresql://melon:MobileCloud!@localhost:5433/postgres")
Sessions = sessionmaker(engine)


#modificare
def get_friendlist(user_id):
    with Sessions() as session:
        try:
            user = session.query(User).get(user_id)
        except Exception as e:
            return {'msg': 'Error while trying to retrieve the user', 'err': str(e)}, 500
        if user is None:
            return {'msg': 'User does not exist'}, 404
        if user.for_confirmation is [] or None:
            return {'msg': "in this section you'll find the sent friend requests"}, 200
        friends = session.query(User).join(
            friendship,
            or_(
                (friendship.c.user == user_id) & (friendship.c.friend_to == User.id),
                (friendship.c.friend_to == user_id) & (friendship.c.user == User.id)
            )
        ).all()
        result = UserSchema().dump(friends, many=True)
        return result, 200


#da modificare
def get_pendinglist(user_id):
    with Sessions() as session:
        try:
            user = session.query(User).get(user_id)
        except Exception as e:
            return {'msg': 'Error while trying to retrieve the user', 'err': str(e)}, 500
        if user is None:
            return {'msg': 'User does not exist'}, 404
        if user.for_confirmation is [] or None:
            return {'msg': "in this section you'll find the sent friend requests"}, 200
        result = UserSchema().dump(user.waiting, many=True)
        return result, 200


def accept_friend_in_pending(user_id, accepted_friendship_by_user_id):
    with Sessions() as session:
        try:
            user = session.query(User).get(user_id)
        except Exception as e:
            return {'msg': 'Error while trying to retrieve the user', 'err': str(e)}, 500
        try:
            accepted_friendship_by_user = session.query(User).get(accepted_friendship_by_user_id)
        except Exception as e:
            return {'msg': 'Error while trying to retrieve the friend', 'err': str(e)}, 500
        if accepted_friendship_by_user not in user.friend_to:
            try:

                user.for_confirmation.remove(accepted_friendship_by_user)

                accepted_friendship_by_user.users.append(user)

                session.commit()
            except Exception as e:
                return {'msg': 'Error while trying to do some action in the DB', 'err': str(e)}, 500
        else:
            return {'msg': "Friend already added"}, 200
        return {'msg': "Request Successfully Accepted"}, 200


def add_friend_in_pending(user_id, sent_friend_request_user_id):
    with Sessions() as session:
        try:
            user = session.query(User).get(user_id)
        except Exception as e:
            return {'msg': 'Error while trying to retrieve the user', 'err': str(e)}, 500
        try:
            sent_friend_request_user = session.query(User).get(sent_friend_request_user_id)
        except Exception as e:
            return {'msg': 'Error while trying to retrieve the friend', 'err': str(e)}, 500
        if sent_friend_request_user not in user.for_confirmation:
            try:
                user.for_confirmation.append(sent_friend_request_user)
                sent_friend_request_user.waiting.append(user)
                session.commit()
            except Exception as e:
                return {'msg': 'Error while trying to do some action in the DB', 'err': str(e)}, 500
        else:
            return {'msg': "Already waiting for confirmation"}, 200
        return {'msg': "Request Successfully Accepted"}, 200


def decline_friend_request(user_id, accepted_friend_id):
    with Sessions() as session:
        try:
            user = session.query(User).get(user_id)
        except Exception as e:
            return {'msg': 'Error while trying to retrieve the user', 'err': str(e)}, 500
        try:
            accepted_friend = session.query(User).get(accepted_friend_id)
        except Exception as e:
            return {'msg': 'Error while trying to retrieve the friend', 'err': str(e)}, 500
        if user in accepted_friend.waiting:
            try:
                accepted_friend.waiting.remove(user)
                session.commit()
            except Exception as e:
                return {'msg': 'Error while trying to do some action in the DB', 'err': str(e)}, 500
        else:
            return {'msg': "Friend not present in pending list"}, 404
        return {'msg': "Request Successfully Accepted"}, 200


def remove_friend_in_friendlist(user_id, remove_friend_id):
    with Sessions() as session:
        try:
            user = session.query(User).get(user_id)
        except Exception as e:
            return {'msg': 'Error while trying to retrieve the user', 'err': str(e)}, 500
        try:
            remove_friend = session.query(User).get(remove_friend_id)
        except Exception as e:
            return {'msg': 'Error while trying to retrieve the friend', 'err': str(e)}, 500
        if remove_friend in user.friend_to:
            try:
                user.friend_to.remove(remove_friend)
                session.commit()
            except Exception as e:
                return {'msg': 'Error while trying to do some action in the DB', 'err': str(e)}, 500
        elif remove_friend in user.users:
            try:
                user.users.remove(remove_friend)
                session.commit()
            except Exception as e:
                return {'msg': 'Error while trying to do some action in the DB', 'err': str(e)}, 500
        else:
            return {'msg': "Friend not present in friendlist"}, 404
        return {'msg': "Request Successfully Accepted"}, 200


def get_user_by_username(nickname):
    with Sessions() as session:
        try:
            result = session.query(User).filter_by(username=nickname).all()
        except Exception as e:
            return {'msg': 'Error while trying to retrieve the user', 'err': str(e)}, 500
        send_result = UserSchema().dump(result, many=True), 200
        return send_result
