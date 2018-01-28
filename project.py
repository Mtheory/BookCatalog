from flask import Flask, render_template, request, redirect, \
                  jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem


app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Show all categories
@app.route('/')
@app.route('/catalog/')
def showCategories():
    catalog = session.query(Category).order_by(asc(Category.id))
    itemsList = session.query(CategoryItem).filter_by(category_id=1).all()
    return render_template('catalog.html', categoryItems=itemsList,
                           catalog=catalog)


@app.route('/catalog/<int:category_id>/')
def showItems(category_id):
    catalog = session.query(Category).order_by(asc(Category.id))
    itemsList = session.query(CategoryItem).filter_by /
    (category_id=category_id).all()
    return render_template('catalog.html', categoryItems=itemsList,
                           catalog=catalog)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
