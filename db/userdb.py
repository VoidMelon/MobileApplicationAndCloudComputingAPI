from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.models import User

engine = create_engine("postgresql://melon:MobileCloud!@localhost/mobile-project")

Session = sessionmaker(engine)


def insert_user_db(user_parameters):
    with Session() as session:
        user = User(**user_parameters)
        try:
            session.add(user)
        except Exception as err:
            return {'msg': "Error during the insertion of the user with error:", 'err': str(err)}, 500
        session.commit()
        return {'msg': "User successfully inserted"}, 200


def delete_user_db(userid):
    with Session() as session:
        try:
            user = session.query(User).get(id)
        except Exception as err:
            return {'msg': "Error during the deletion of the user: with error:", 'err': str(err)}, 404
        try:
            session.delete(user)
        except Exception as err:
            return {'msg': "Error during the deletion of the user: with error:", 'err': str(err)}, 500
        return {'msg': "User successfully deleted"}, 200
