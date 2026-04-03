# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


#__MODELS__
class Livro(db.Model):

    __tablename__ = 'Livro'

    id = db.Column(db.Integer, primary_key=True)

    #__Livro_FIELDS__
    isbn = db.Column(db.Integer, nullable=True)
    titulo = db.Column(db.String(255),  nullable=True)
    resumo_sinopse = db.Column(db.Text, nullable=True)
    ano_publicacao = db.Column(db.DateTime, default=db.func.current_timestamp())
    edicao = db.Column(db.Integer, nullable=True)
    preco_venda = db.Column(db.Integer, nullable=True)
    preco_compra = db.Column(db.Integer, nullable=True)
    quantidade_estoque = db.Column(db.Integer, nullable=True)
    formato = db.Column(db.String(255),  nullable=True)
    id_editora = db.Column(db.Integer, nullable=True)

    #__Livro_FIELDS__END

    def __init__(self, **kwargs):
        super(Livro, self).__init__(**kwargs)



#__MODELS__END
