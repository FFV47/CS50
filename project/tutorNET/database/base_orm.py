from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("sqlite:///database/tutorNET.sqlite")
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
# Allow session.query(Foo) to be shorthanded Foo.query
Base.query = db_session.query_property()


def init_db():
    import database.tables

    Base.metadata.create_all(engine)
