import datetime
from sqlalchemy import DATE, VARCHAR, Column, Integer, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Posts(Base):
    __tablename__ = 'post'

    post_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    status = Column(VARCHAR(4), unique=False, nullable=False, default='wait')
    post_type = Column(VARCHAR(3), unique=False, nullable=False)
    link = Column(Text, unique=True, nullable=False)
    reg_date = Column(DATE, default=datetime.datetime.now())
