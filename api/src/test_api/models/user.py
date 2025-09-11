from sqlalchemy import Column, Integer, String, DateTime
from test_api.db.connection import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    date_of_birth = Column(DateTime(timezone=True), nullable=False)