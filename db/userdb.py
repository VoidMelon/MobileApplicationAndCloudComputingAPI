from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

from model.models import User, UserSchema

# engine = create_engine("postgresql://melon:MobileCloud!@localhost/mobile-project")
# engine = create_engine("postgresql://melon:MobileCloud!@localhost:5433/postgres")
# 93.147.17.126:6000
# engine = create_engine("postgresql://postgres:MobileCloud!@192.168.1.250:5432/postgres")
engine = create_engine("postgresql://postgres:MobileCloud!@93.147.17.126:6000/postgres")

Session = sessionmaker(engine)


def insert_user_db(user_parameters):
    with Session() as session:
        user = User(**user_parameters)
        try:
            session.add(user)
        except Exception as err:
            session.rollback()
            return {'msg': "Error during the insertion of the user with error:", 'err': str(err)}, 500
        session.commit()
        return {'msg': "User successfully inserted"}, 200


def delete_user_db(userid):
    with Session() as session:
        try:
            user = session.query(User).get(userid)
        except Exception as err:
            return {'msg': "User Not Found", 'err': str(err)}, 404
        try:
            session.delete(user)
        except Exception as err:
            session.rollback()
            return {'msg': "Error during the deletion of the user: with error:", 'err': str(err)}, 500
        session.commit()
        return {'msg': "User successfully deleted"}, 200


def get_user_db(userid):
    with Session() as session:
        try:
            user = session.query(User).get(userid)
        except Exception as err:
            session.rollback()
            return {'msg': "Error during the retrieving of the user: with error:", 'err': str(err)}, 500
        if user is None:
            return {'msg': "User does not exist"}, 404
        result = UserSchema().dump(user)
        # user_dictionary = user.__dict__
        # keys = list(user_dictionary.keys())
        # user_dictionary.pop(keys[0])
        # user_dictionary = dict(user_dictionary)
        # user_dictionary["sign_up_date"] = str(datetime_string)
        # print(user_dictionary)
        # print(type(user_dictionary))
        # json_formatted_user = json.dumps(user_dictionary, sort_keys=True)
        return result, 200


def update_user_db(userid, user_parameters):
    with Session() as session:
        try:
            user = session.query(User).get(userid)
        except Exception as err:
            session.rollback()
            return {'msg': "Error while trying to retrieve the user", 'err': str(err)}, 404
        if user is None:
            return {'msg': "User does not exist"}, 404
        print(user_parameters)
        print(type(user_parameters))
        for key, value in user_parameters.items():
            if hasattr(user, key):
                setattr(user, key, value)
        session.commit()
        return {'msg': "User successfully updated"}, 200
