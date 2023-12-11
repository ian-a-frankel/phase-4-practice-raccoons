from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Raccoon(db.Model, SerializerMixin):
    __tablename__ = 'raccoons_table'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False, unique = True)
    age = db.Column(db.Integer, nullable = False)
    @validates('age')
    def validate_name(self, key, val):
        if val > 0:
            return val
        else:
            raise ValueError('age must be greater than 0')
        
    serialize_rules = ('-visits.raccoon',)

    visits = db.relationship('Visit', back_populates = 'Raccoon')

    trashcans = association_proxy('visits', 'trashcan')

class Visit(db.Model, SerializerMixin):
    __tablename__ = 'visits_table'
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.String)
    raccoon_id = db.Column(db.Integer, db.ForeignKey('raccoons_table.id'))
    visit_id = db.Column(db.Integer, db.ForeignKey('trashcans_table.id'))

    serialize_rules = ('-raccoon.visit','-trashcan.visit',)

    raccoon = db.relationship('Raccoon', back_populates = 'visits')
    trashcan = db.relationship('Raccoon', back_populates = 'visits')

class Trashcan(db.Model, SerializerMixin):
    __tablename__ = 'trashcans_table'
    id = db.Column(db.Integer, primary_key = True)
    address = db.Column(db.String)

    serialize_rules = ('-visits.trashcan',)

    visits = db.relationship('Visit', back_populates = 'trashcan')

    raccoons = association_proxy('visits', 'raccoon')