from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

engine = create_engine('sqlite:///vismatools.db?check_same_thread=False')
Base.metadata.bind = engine
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


class BankStatement(Base):
    __tablename__ = 'bank_statement'
    __tableargs__ = {'comment': 'Bank Statements'}

    bank_statement_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    title = Column(String(128), comment='Bank Statement name')
    summary = Column(String(128), comment='Summary')
    date = Column(String(128), default=datetime.utcnow(), comment='data')

    def __repr__(self):
        return f'{self.bank_statement_id} {self.title} {self.summary} {self.date}'


class Settings(Base):
    __tablename__ = 'settings'
    __tableargs__ = {'comment': 'Filter installningar'}
    quote_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    konto = Column(Integer, default=datetime.utcnow(), comment='konto number', unique=True)
    filter = Column(Text, default=datetime.utcnow(), comment='name')

    def __repr__(self):
        return f'{self.konto} {self.filter}'


class Transaktions(Base):
    __tablename__ = 'transaktions'
    __tableargs__ = {'comment': 'transaktions'}
    quote_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    bank_statement_id = Column(Integer, ForeignKey('bank_statement.bank_statement_id'), comment='Bank Statement')
    bank_statement = relationship('BankStatement', backref='quote_author', lazy='subquery')
    tr_date = Column(String(128), default=datetime.utcnow(), comment='data')
    tr_name = Column(String(128), default=datetime.utcnow(), comment='name')
    tr_amount = Column(String(128), default=datetime.utcnow(), comment='amount')
    konto_p = Column(String(128), default=datetime.utcnow(), comment='Primary konto')
    konto_s = Column(String(128), default=datetime.utcnow(), comment='Secondary konto')
    moms = Column(String(1), default=datetime.utcnow(), comment='Moms')

    def __repr__(self):
        return f'{self.tr_name} {self.bank_statement_id}'
