from sqlalchemy import Column, Integer, String
from app.database import Base

class Cryptid(Base):
    __tablename__="cryptids"

    id = Column(Integer, primary_key=True, index=True)
    name=Column(String, index=True)
    description = Column(String)
    image_url = Column(String)