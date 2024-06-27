from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.models import User, SessionSchema, Session

# engine = create_engine("postgresql://melon:MobileCloud!@localhost/mobile-project")
# engine = create_engine("postgresql://melon:MobileCloud!@localhost:5433/postgres")
# engine = create_engine("postgresql://postgres:MobileCloud!@192.168.1.250:5432/postgres")
engine = create_engine("postgresql://postgres:MobileCloud!@93.147.17.126:6000/postgres")
Sessions = sessionmaker(engine)


def insert_session_db(userid, session_parameters):
    with Sessions() as s:
        try:
            user = s.query(User).get(userid)
        except Exception as err:
            return {'msg': "Error occured while trying to retrieve the user", 'err': str(err)}, 500
        if user is None:
            return {'msg': "User does not exist"}, 404
        session = Session(**session_parameters)
        try:
            session.creator = user
            s.add(session)
            user.sessions.append(session)
            s.commit()
        except Exception as err:
            s.rollback()
            return {'msg': "Error occurred while trying to insert a session", 'err': str(err)}, 500
        return {"id": session.id, "msg": "Session successfully inserted"}, 201


def delete_session_db(user_id, session_id):
    with Sessions() as s:
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
                session.environment_data = []
                s.delete(session)
                s.commit()
        except Exception as err:
            s.rollback()
            return {'msg': "Error occurred while trying to delete a session", 'err': str(err)}, 500
        return {'msg': "Session successfully deleted"}, 200


def get_session_db(user_id, session_id):
    with Sessions() as s:
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
        result = SessionSchema().dump(session)
        return result, 200
        # return dict(session), 200


def get_all_sessions_db(user_id):
    with Sessions() as s:
        try:
            user = s.query(User).get(user_id)
        except Exception as err:
            return {'msg': "User does not exist", 'err': str(err)}, 404
        sessions_created = user.sessions
        if sessions_created is None:
            sessions_created = []
            return SessionSchema().dump(sessions_created, many=True)
        result = SessionSchema().dump(sessions_created, many=True)
        return result, 200


def update_session_db(user_id, session_id, session_parameters):
    with Sessions() as s:
        try:
            user = s.query(User).get(user_id)
        except Exception as err:
            return {'msg': "Error during the retrieving of the user", 'err': str(err)}, 500
        try:
            session = s.query(Session).get(session_id)
        except Exception:
            return {'msg': "Error during the retrieving of the session"}, 500
        if session not in user.sessions:
            return {'msg': "Denied"}, 403
        for key, value in session_parameters.items():
            if hasattr(session, key):
                setattr(session, key, value)
        s.commit()
        return {'msg': "Session successfully updated"}, 200

