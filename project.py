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



#JSON APIs to view Catalog/Category Information
@app.route('catalog/JSON')
def showCategories():
    catalog = session.query(Category).order_by(asc(Category.id))
    
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    Menu_Item = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(Menu_Item = Menu_Item.serialize)

@app.route('/restaurant/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants= [r.serialize for r in restaurants])


# Show all categories
@app.route('/')
@app.route('/catalog/', methods=['GET','POST'])
def showCategories():
    catalog = session.query(Category).order_by(asc(Category.id))
    itemsList = session.query(CategoryItem).filter_by(category_id=1).all()
    index = 1
    return render_template('catalog.html', categoryItems=itemsList,
                           catalog=catalog, index = index)


# Show selected category and associated books
@app.route('/catalog/<int:category_id>/', methods=['GET','POST'])
def showItems(category_id):
    catalog = session.query(Category).order_by(asc(Category.id))
    itemsList = session.query(CategoryItem).filter_by(
                category_id=category_id).all()
    return render_template('catalog.html', categoryItems=itemsList,
                           catalog=catalog, index = category_id)


# Show book description and details
@app.route('/catalog/<int:category_id>/book/<int:book_id>', methods=['GET','POST'])
def showDescription(category_id, book_id):
    category = session.query(Category).filter_by(id = category_id).one()
    item = session.query(CategoryItem).filter_by(id = book_id).one()
    return render_template('description.html', book=item, category=category)


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
@app.route('/catalog/<int:category_id>/addbook/', methods=['GET','POST'])
def addBook(category_id):
    selectedCategory = session.query(Category).filter_by(id = category_id).one()
    if request.method == 'POST':
        newBook = CategoryItem(name = request.form['name'], author = request.form['author'], description = request.form['description'], category_id = category_id)
        session.add(newBook)
        session.commit()
        flash('New Book %s Successfully Created' % newBook.name)
        return redirect(url_for('showItems', category_id = category_id))
    else:
        return render_template('addBook.html', category_id = category_id, category_name = selectedCategory.name)


# Edit a book
@app.route('/catalog/<int:category_id>/book/<int:book_id>/edit', methods=['GET','POST'])
def editBook(category_id, book_id):
    selectedCategory = session.query(Category).filter_by(id = category_id).one()
    book = session.query(CategoryItem).filter_by(id = book_id).one()
    if request.method == 'POST':
        if request.form['name']:
            book.name = request.form['name']
        if request.form['author']:
            book.author = request.form['author']
        if request.form['description']:
            book.description = request.form['description']
        flash('Book %s Successfully Edited' % book.name)
        return render_template('description.html', book = book, category = selectedCategory)
    else:
        return render_template('editBook.html', book = book, category = selectedCategory )


# Delete a book
@app.route('/catalog/<int:category_id>/book/<int:book_id>/delete', methods=['GET','POST'])
def deleteBook(category_id, book_id):
    selectedCategory = session.query(Category).filter_by(id = category_id).one()
    bookToDelete = session.query(CategoryItem).filter_by(id = book_id).one()
    if request.method == 'POST':
        session.delete(bookToDelete)
        flash('Book %s Successfully Deleted' % bookToDelete.name)
        session.commit()
    return redirect(url_for('showItems', category_id = category_id))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
