import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from flask_migrate import Migrate





database_name = "capstone_database"

database_path = "postgresql://{}:{}@{}/{}".format(
    'oltda', 'janaoltova', 'localhost:5432', database_name)


db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Warehouse(db.Model):
    __tablename__ = 'warehouse'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    stock_items = db.relationship('StockItems', backref='warehouse', lazy=True)

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

class StockItems(db.Model):
    __tablename__ = 'stock_items'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String)
    quantity = db.Column(db.Integer)
    expiration_date = db.Column(db.Date, nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'))
    product_code = db.Column(db.String, db.ForeignKey('product_codes.product_code'))

    def __init__(self, product_name, quantity, expiration_date, warehouse_id, product_code):
        self.product_name = product_name
        self.quantity = quantity
        self.expiration_date = expiration_date
        self.warehouse_id = warehouse_id
        self.product_code = product_code

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

class ProductCodes(db.Model):
    __tablename__ = 'product_codes'

    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String, unique=True)
    description = db.Column(db.String)
    unit = db.Column(db.String)
    stock_items = db.relationship('StockItems', backref='product_codes', lazy=True)

    def __init__(self, product_code, description, unit):
        self.product_code = product_code
        self.description = description
        self.unit = unit


    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

