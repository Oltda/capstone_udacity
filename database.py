import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from flask_migrate import Migrate
from dotenv import load_dotenv
from dataclasses import dataclass
import os
from dotenv import load_dotenv


load_dotenv()
database_path = os.environ.get('DATABASE_URL')

database_name = "capstone_database"

database_path = "postgres://ofapcuhmthwgzf:4dad289b111001edc5d9534f8ac3e396f6a662b0f6c3cc7ea00d3087b38a4c33@ec2-52-4-111-46.compute-1.amazonaws.com:5432/d5vufr3v9884d9"

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()




class DatabaseOprations(db.Model):
    __abstract__ = True

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


@dataclass
class Warehouse(DatabaseOprations):
    id: int
    name: String
    address: String

    __tablename__ = 'warehouse'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    stock_items = db.relationship('StockItems', backref='warehouse', lazy=True)


@dataclass
class StockItems(DatabaseOprations):
    id = int
    product_name = String
    quantity = int
    expiration_date = String
    warehouse_id = int
    product_code = String

    __tablename__ = 'stock_items'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String)
    quantity = db.Column(db.Integer)
    expiration_date = db.Column(db.Date, nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'))
    product_code = db.Column(db.String, db.ForeignKey('product_codes.product_code'))


@dataclass
class ProductCodes(DatabaseOprations):
    id = int
    product_code = String
    description = String
    unit = String

    __tablename__ = 'product_codes'

    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String, unique=True)
    description = db.Column(db.String)
    unit = db.Column(db.String)
    stock_items = db.relationship('StockItems', backref='product_codes', lazy=True)
