from sqlalchemy import Integer, String
from sqlalchemy.sql.schema import Column
from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)


