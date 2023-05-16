from sqlalchemy import create_engine, Column, BigInteger, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://pguser:pguser@localhost:25500/pgol")


def make_session():
    Session = sessionmaker(engine)
    session = Session()
    try:
        return session
    finally:
        session.close()


Base = declarative_base()


class Member(Base):
    __tablename__ = "Members"
    id = Column(BigInteger, primary_key=True, index=True)
    firstname = Column(Text)
    middlename = Column(Text)
    surname = Column(Text)
    group = Column(Text)


class Team(Base):
    __tablename__ = "Teams"
    id = Column(BigInteger, primary_key=True, index=True)
    id1 = Column(BigInteger)
    id2 = Column(BigInteger)
    id3 = Column(BigInteger)
    surnames = Column(Text)


Base.metadata.create_all(bind=engine)
