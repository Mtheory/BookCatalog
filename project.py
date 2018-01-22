from flask import Flask
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem


app = Flask(__name__)


# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

'''
@app.route('/')
def catalog():
    query = session.query(Category)
    output = ''
    for i in query:
        output += '</br>'
        output += i.name
        output += " " + str(i.id)
        output += '</br>'
    return output

@app.route('/category/<int:category_id>/')
def catalogList(category_id):
    cat= session.query(Category).filter_by(id=category_id).one()
    categoryItems=session.query(CategoryItem).filter_by(category_id=cat.id)
    output = ''
    for i in categoryItems:
        output += i.name
        output += '</br>'
        output += i.description
        output += '</br>'
        output += '</br>'
    return output
    '''


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
