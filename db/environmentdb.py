from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.models import User, Session, EnvironmentDataSchema, EnvironmentData

# engine = create_engine("postgresql://melon:MobileCloud!@localhost/mobile-project")
engine = create_engine("postgresql://melon:MobileCloud!@localhost:5433/postgres")
Sessions = sessionmaker(engine)


def insert_environment_data_db(user_id, session_id, environment_parameters):
    with Sessions() as s:
        try:
            user = s.query(User).get(user_id)
            print(user is None)
        except Exception as err:
            return {'msg': "Error while trying to retrieve user", 'err': str(err)}, 500
        try:
            session = s.query(Session).get(session_id)
            print(session is None)
            print(user is None or session is None)
        except Exception as err:
            return {'msg': "Error while trying to retrieve session", 'err': str(err)}, 500
        if user is None or session is None:
            return {'msg': "User or Session do not exist"}, 404
        environment = EnvironmentData(**environment_parameters)
        session.environment_data.append(environment)
        try:
            s.add(environment)
        except Exception as err:
            return {'msg': "Error while trying to add environment data", 'err': str(err)}, 500
        s.commit()
        return {'msg': 'Data successfully inserted'}, 200


def get_last_environment_data_db(user_id, session_id):
    with Sessions() as s:
        try:
            user = s.query(User).get(user_id)
        except Exception as err:
            return {'msg': "Error while trying to retrieve user", 'err': str(err)}, 500
        try:
            session = s.query(Session).get(session_id)
        except Exception as err:
            return {'msg': "Error while trying to retrieve session", 'err': str(err)}, 500
        if session not in user.sessions:
            return {'msg': "Session does not exist"}, 404
        if session.environment_data is None or len(session.environment_data) == 0:
            environment_data_list_empty = []
            return EnvironmentDataSchema.dump(environment_data_list_empty)
        return EnvironmentDataSchema().dump(session.environment_data[-1]), 200


def get_all_environment_data_db(user_id, session_id):
    with Sessions() as s:
        try:
            user = s.query(User).get(user_id)
        except Exception as err:
            return {'msg': "Error while trying to retrieve user", 'err': str(err)}, 500
        try:
            session = s.query(Session).get(session_id)
        except Exception as err:
            return {'msg': "Error while trying to retrieve session", 'err': str(err)}, 500
        if session not in user.sessions:
            return {'msg': "Session does not exist"}, 404
        if session.environment_data is None:
            environment_data_list_empty = []
            return EnvironmentDataSchema().dump(environment_data_list_empty)
        result = EnvironmentDataSchema().dump(session.environment_data, many=True)
        return result, 200
