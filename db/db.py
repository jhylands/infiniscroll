from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager
import os

engine = create_engine('mysql://timepcou_site:{}@141.136.33.223/timepcou_devopchallenge?charset=utf8&use_unicode=1'.format(os.environ["code"]))
Session = scoped_session(sessionmaker(bind=engine))

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
