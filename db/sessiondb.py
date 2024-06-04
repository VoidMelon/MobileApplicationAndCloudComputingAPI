from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.models import User

engine = create_engine("postgresql://melon:MobileCloud!@localhost/mobile-project")

Session = sessionmaker(engine)


def insert_session_db(user_id, session_parameters):
    with Session() as s:
        try:
            user = s.query(User).get(user_id)
        except Exception as err:
            return {'msg': "Error occured while trying to retrieve the user", 'err': str(err)}, 500
        if user is None:
            return {'msg': "User does not exist"}, 404
        session = Session(**session_parameters)
        try:
            s.add(session)
            user.sessions.append(session)
        except Exception as err:
            s.rollback()
            return {'msg': "Error occurred while trying to insert a session", 'err': str(err)}, 500
        s.commit()
        return {'msg': "Session successfully inserted"}, 201


def delete_session_db(user_id, session_id):
    with Session() as s:
        try:
            user = s.query(User).get(user_id)
        except Exception as err:
            return {'msg': "Error occurred while trying to retrieving the user", 'err': str(err)}, 500
        if user is None:
            return {'msg': "User does not exist", 'err': "User does not exist"}, 404
        session = s.query(Session).get(session_id)
        if session is None:
            return {'msg': "Session does not exist"}, 404
        try:
            if session in user.sessions:
                user.sessions.remove(session)
                s.delete(session)
        except Exception as err:
            s.rollback()
            return {'msg': "Error occurred while trying to delete a session", 'err': str(err)}, 500
        s.commit()
        return {'msg': "Session successfully deleted"}, 200


def get_session_db(user_id, session_id):
    with Session() as s:
        try:
            user = s.query(User).get(user_id)
        except Exception as err:
            return {'msg': "Error occurred while trying to retrieving the user", 'err': str(err)}, 500
        if user is None:
            return {'msg': "User does not exist"}, 404
        try:
            session = s.query(Session).get(session_id)
        except Exception as err:
            return {'msg': "Error occurred while trying to retrieving the session", 'err': str(err)}, 500
        if session is None:
            return {'msg': "Session does not exist"}, 404
        return dict(session), 200

def get_all_sessions_db(user_id):
    with Session() as s:
        try:
            user = s.query(User).get(user_id)
        except Exception as err:
            return {'msg': "User does not exist", 'err': str(err)}, 404
        sessions_created = user.sessions
        if sessions_created is None:
            sessions_created = []
            return sessions_created
        return sessions_created
