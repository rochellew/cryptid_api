from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Main database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./cryptids.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db(engine_override=None):
    # Use the provided engine if given (for testing)
    db = SessionLocal() if not engine_override else sessionmaker(autocommit=False, autoflush=False, bind=engine_override)()
    try:
        yield db
    finally:
        db.close()
