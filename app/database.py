from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Main database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./cryptids.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    # Use the provided engine if given (for testing)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
