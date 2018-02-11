from flask import Flask, render_template, request, redirect, \
                  jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem


app = Flask(__name__)
app.secret_key = 'some_secret'

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
    index = 1
    return render_template('catalog.html', categoryItems=itemsList,
                           catalog=catalog, index = index)


# show selected category and associated items
@app.route('/catalog/<int:category_id>/', methods=['GET','POST'])
def showItems(category_id):
    catalog = session.query(Category).order_by(asc(Category.id))
    itemsList = session.query(CategoryItem).filter_by(
                category_id=category_id).all()
    return render_template('catalog.html', categoryItems=itemsList,
                           catalog=catalog, index = category_id)


# Show book description
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
        flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('addCategory.html')


# Edit a selected category
@app.route('/catalog/<int:category_id>/edit/', methods = ['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(Category).filter_by(id = category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            flash('Category Successfully Edited %s' % editedCategory.name)
        return redirect(url_for('showItems', category_id = category_id))
    else:
        return render_template('editCategory.html', category_id = category_id, category_name = editedCategory.name )


# Delete category
@app.route('/catalog/<int:category_id>/delete/', methods=['GET','POST'])
def deleteCategory(category_id):
    selectedCategory = session.query(Category).filter_by(id = category_id).one()
    #itemToDelete = session.query(CategoryItem).filter_by(id = book_id).all()
    if request.method == 'POST':
        session.delete(selectedCategory)
        flash('%s Successfully Deleted' % selectedCategory.name)
        session.commit()
    return redirect(url_for('showCategories'))


# Add a new book


# Edit a book


# Delete a book


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
