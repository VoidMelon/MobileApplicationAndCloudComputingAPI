from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://melon:MobileCloud!@localhost/mobile-project")

Session = sessionmaker(engine)


def insert_session_db(session_parameters):
    with Session() as s:
        session = Session(**session_parameters)
        try:
            s.add(session)
        except Exception as err:
            return {'msg': "Error occurred while trying to insert a session"}, 500
        return {'msg': "Session successfully inserted"}, 201
