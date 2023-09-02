from sqlalch_db import SessionContextManger
from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, String, Boolean, Column
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalch_db import engine1

Base = declarative_base()

class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default='NOW()')
    last_modified = Column(TIMESTAMP(timezone=True), nullable=False, server_default='NOW()')
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default='NOW()')
    last_modified = Column(TIMESTAMP(timezone=True), nullable=False, server_default='NOW()')
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_reset = Column(Boolean, server_default="FALSE")

Base.metadata.create_all(engine1)
