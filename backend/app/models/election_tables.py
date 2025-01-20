import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, text

Base = declarative_base()

# people = Table(
#     "people",
#     ,
#     Column("id", Integer, primary_key=True),
#     Column("name", String),
#     Column("Age", Integer),
#     Column("Gender", String(1)),
# )
class Electors(Base):
    __tablename__ = "elctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    veriffKey = Column(String, nullable=False)

class ElectoralRoll(Base):
    __tablename__ = "electoral_roll"
    id = Column(Integer, primary_key=True, index=True)
    pk = Column(String, nullable=False)
    pin = Column(String, nullable=False)

# class BulletinBorad(Base):
#     __tablename__= "bulletin_board"
#     id = Column(Integer, primary_key=True, index=True)
#     tag = Column(String, nullable=False)
#     content = Column(String, nullable=False)

class AllBallots(Base):
    __tablename__= "all_ballots"
    id = Column(Integer, primary_key=True, index=True)
    revocated = Column(String, primary_key=True, index=True)
    pk = Column(String, nullable=False)
    pin = Column(String, nullable=False)
    candidate = Column(String, nullable=False)

class ShuffleBallots(Base):
    __tablename__="shuffled_ballots"
    id = Column(Integer, primary_key=True, index=True)
    candidate = Column(String, nullable=False)

class RevocatedBallots(Base):
    __tablename__ = "revocation"
    id = Column(Integer, primary_key=True, index=True)
    pk = Column(String, nullable=False)
    pin = Column(String, nullable=False)
    candidate = Column(String, nullable=False)


class TestTable(Base):
    __tablename__= "test_table"
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String, nullable=False)
    content = Column(String, nullable=False)