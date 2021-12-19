import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    chat_id = Column(String(20), nullable=False)
    lang = Column(String(7))
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, name, chat_id, lang):
        self.name = name
        self.chat_id = chat_id
        self.lang = lang

    def __repr__(self):
        return f'<User {self.id}: {self.name}>'


class SubscriptionMode(enum.Enum):
    none = 0
    new_work_of_author = 1
    new_chapter_of_work = 2
    new_chapter_of_author = 3

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented


class Subscription(Base):
    __tablename__ = 'subscription'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    mode = Column(Enum(SubscriptionMode), nullable=False)
    author_oid = Column(String(16), nullable=True)
    work_oid = Column(Integer, nullable=True)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User', backref=backref('subscriptions'))

    def __init__(self, user_id, mode, author_oid=None, work_oid=None):
        self.user_id = user_id
        self.mode = mode
        self.author_oid = author_oid
        self.work_oid = work_oid

    def __repr__(self):
        return f'<Subscription {self.id} | {self.user.id}-{self.user.name}> '


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_oid = Column(String(16), nullable=False)
    last_fetch_time = Column(DateTime)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, author_oid):
        self.author_oid = author_oid

    def __repr__(self):
        return f'<Author: {self.author_oid}>'


class Work(Base):
    __tablename__ = 'work'

    id = Column(Integer, primary_key=True, autoincrement=True)
    work_oid = Column(Integer, nullable=False)
    name = Column(String(32), nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'))
    pub_date = Column(DateTime)
    # fandoms
    # symbols
    # language
    words = Column(Integer)
    chapter_count = Column(Integer)
    kudos = Column(Integer)
    hits = Column(Integer)
    last_fetch_time = Column(DateTime)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    author = relationship('Author', backref=backref('works'))

    def __init__(self, work_oid, name, author_id, pub_date, words, chapter_count, kudos, hits):
        self.work_oid = work_oid
        self.name = name
        self.author_id = author_id
        self.pub_date = pub_date
        self.words = words
        self.chapter_count = chapter_count
        self.kudos = kudos
        self.hits = hits

    def __repr__(self):
        return f'<Work: {self.name} | {self.author.author_oid}>'


class Chapter(Base):
    __tablename__ = 'chapter'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chapter_id = Column(Integer, nullable=False)
    name = Column(String(32), nullable=False)
    work_id = Column(Integer, ForeignKey('work.id'))
    pub_date = Column(DateTime)
    summary = Column(Text)
    content = Column(Text, nullable=False)
    last_fetch_time = Column(DateTime)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    work = relationship('Work', backref=backref('chapters'))

    def __init__(self, chapter_id, name, work_id, pub_date, summary, content):
        self.chapter_id = chapter_id
        self.name = name
        self.pub_date = pub_date
        self.work_id = work_id
        self.summary = summary
        self.content = content

    def __repr__(self):
        return f'<Chapter: {self.name} | {self.work.name}>'
