from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date, DateTime, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


# class Topic(Base):
#     __tablename__ = 'topic'
#     __tableargs__ = {'comment': 'Темы цитат'}
#
#     topic_id = Column(
#         Integer,
#         nullable=False,
#         unique=True,
#         primary_key=True,
#         autoincrement=True
#     )
#     name = Column(String(128), comment='Наименование темы')
#     description = Column(Text, comment='Описание темы')
#
#     def __repr__(self):
#         return f'{self.topic_id} {self.name} {self.description}'


class BankStatement(Base):
    __tablename__ = 'bank_statement'
    __tableargs__ = {'comment': 'Bank Statements'}

    bank_statement_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    title = Column(String(128), comment='Bank Statement name')
    summary = Column(String(128), comment='Summary')
    date = Column(String(128), default=datetime.utcnow(), comment='data')

    def __repr__(self):
        return f'{self.bank_statement_id} {self.title} {self.summary} {self.date}'


class Transaktions(Base):
    __tablename__ = 'Transaktions'
    __tableargs__ = {'comment': 'Transaktions'}
    quote_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    text = Column(Text, comment='#####')
    bank_statement_id = Column(Integer, ForeignKey('bank_statement.bank_statement_id'), comment='Bank Statement')
    bank_statement = relationship('BankStatement', backref='quote_author', lazy='subquery')

    def __repr__(self):
        return f'{self.text} {self.bank_statement_id}'





