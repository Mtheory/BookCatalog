from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem


#Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/hello')
def HelloWorld():
    return "Hello World"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
