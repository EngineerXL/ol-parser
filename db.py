from sqlalchemy import create_engine, select, Column, BigInteger, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import EmailType

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
    nickname = Column(Text)
    email = Column(EmailType)
    login = Column(Text)
    password = Column(Text)
    mail_sent = Column(Boolean, default=False)


def make_stmt(member):
    return select(Member).where(
        Member.surname == member["surname"],
        Member.firstname == member["firstname"],
        Member.middlename == member["middlename"],
        Member.group == member["group"],
        Member.email == member["email"],
    )


def make_nickname(member):
    ar = [
        member["surname"],
        member["firstname"],
        member["middlename"],
        member["group"],
    ]
    return " ".join([elem for elem in ar if elem is not None])


def make_db_member(member):
    return Member(
        surname=member["surname"],
        firstname=member["firstname"],
        middlename=member["middlename"],
        group=member["group"],
        email=member["email"],
        nickname=make_nickname(member),
        login=member["login"],
        password=member["password"],
    )


class Team(Base):
    __tablename__ = "Teams"
    id = Column(BigInteger, primary_key=True, index=True)
    id1 = Column(BigInteger)
    id2 = Column(BigInteger)
    id3 = Column(BigInteger)
    surnames = Column(Text)


Base.metadata.create_all(bind=engine)
