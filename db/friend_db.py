from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.models import User, Session, EnvironmentDataSchema, EnvironmentData

# engine = create_engine("postgresql://melon:MobileCloud!@localhost/mobile-project")
engine = create_engine("postgresql://melon:MobileCloud!@localhost:5433/postgres")
Sessions = sessionmaker(engine)