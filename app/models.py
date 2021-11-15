from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy import Column, Integer, String, Boolean, DATE, DDL


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    checkin = Column(TIMESTAMP(timezone=True),
                     nullable=False, server_default=text('now()'))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class UserStatus(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, nullable=False)
    last_checkin = Column(TIMESTAMP(timezone=True),
                          nullable=False, server_default=text('now()'))
