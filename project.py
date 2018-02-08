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
@app.route('/catalog/', methods=['GET','POST'])
def showCategories():
    catalog = session.query(Category).order_by(asc(Category.id))
    itemsList = session.query(CategoryItem).filter_by(category_id=1).all()
    return render_template('catalog.html', categoryItems=itemsList,
                           catalog=catalog)


@app.route('/catalog/<int:category_id>/', methods=['GET','POST'])
def showItems(category_id):
    catalog = session.query(Category).order_by(asc(Category.id))
    itemsList = session.query(CategoryItem).filter_by(
                category_id=category_id).all()
    index = category_id
    return render_template('catalog.html', categoryItems=itemsList,
                           catalog=catalog, index = index)


@app.route('/catalog/<int:category_id>/book/<int:book_id>', methods=['GET','POST'])
def showDescription(category_id, book_id):
    category = session.query(Category).filter_by(id = category_id).one()
    item = session.query(CategoryItem).filter_by(id = book_id).one()
    return render_template('description.html', item=item, category=category)

# Create a new category
@app.route('/catalog/new/', methods=['GET','POST'])
def newCategory():
  if request.method == 'POST':
      newCategory = Category(name = request.form['name'])
      session.add(newCategory)
      #flash('New Category %s Successfully Created' % newCategory.name)
      session.commit()
      return redirect(url_for('showCategories'))
  else:
      return render_template('addCategory.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
