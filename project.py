from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   jsonify,
                   url_for,
                   flash)
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
import requests
import json


app = Flask(__name__)
app.secret_key = '123Gvt45Ctd67MlerT56TG9'

# clientID will reference client_secrets.json file
CLIENT_ID = json.loads(open('client_secrets.json', 'r').
                       read())['web']['client_id']
APPLICATION_NAME = "Book Catalog Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# routnig for login and create an anti forgery token: state variable.
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# google login
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # confirm that the token that the client sends to the server matches
    # the token that the server sent to the client.
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # collect the one time code from my server
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    # If an error happens along the way, then i will throw this flow exchange
    # FlowExchangeError and send the response as JSON object.
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    # append this token to the following Google URL, the Google API server can
    # verify that this is a valid token for use.
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # if my result contains any errors, then send the 500 Internal
    # Server Error to the client.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # check if we have the right access token.
    gplus_id = credentials.id_token['sub']
    # grab the ID of the token in my credentials object
    # compare it to the ID returned by the Google API server. If these two
    # ID's do not match the i do not have the correct token
    # and should return an error.
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # check to see if user is alread logged in. This will return a 200
    # Successful authentication without resetting all of the login
    # session variables again.
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # in login session store credentials, Google Plus ID.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # using Google Plus API get some more information aout user
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # store the user datat hat we are interested
    login_session['username'] = data['name']
    login_session['email'] = data['email']

    # check if user exists, if it doesn't make a new None
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'

    # flash message to let the user know that they are logged in.
    flash("You are now logged as %s" % login_session['username'])
    print "done!"
    return output


# disconnect the user from Google account
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a conneected user
    access_token = login_session.get('access_token')
    # if the acccess_token is empty we don't have record of a user, so there
    # is no diconnect from the application
    if access_token is None:
        print 'Access Token is None'  # return a 401 error for this case
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    # acces token and pass it into google's url for revoking
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
          % login_session['access_token']
    h = httplib2.Http()
    # now store Google's response in an object called result
    result = h.request(url, 'GET')[0]

    # if response of 200 was received then succesfully diconected
    if result['status'] == '200':
        # delete teh credentials .gplus_id ...etc
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        # create a response to indicate that a user successfully logged out
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successfully disconnected")
        return showCategories()
    else:
        # if getting other response than 200 , the somthing went worng
        # and return a 00 message to the client with sttment of what happened
        response = make_response(json.dumps(
                    'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# creates a new user in our database extracting all of the fields necessary
# from login_session to populate all the values required. In Next
# step returns the user ID of new user created.
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# returns the user object associated with user_id given as an argument
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# returns user ID  if email in the argument is recorded in User tabl
# if not then returns none.
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# JSON APIs to view Catalog/Category Information
@app.route('/catalog/JSON')
def categoriesJSON():
    catalog = session.query(Category).order_by(asc(Category.id))
    return jsonify(Catalog=[c.serialize for c in catalog])


@app.route('/catalog/usersJSON')
def usersJSON():
    users = session.query(User).order_by(asc(User.id))
    return jsonify(User=[c.serialize for c in users])


@app.route('/catalog/<int:category_id>/JSON')
def categoryBooksJSON(category_id):
    catalog = session.query(Category).order_by(asc(Category.id))
    itemsList = session.query(CategoryItem).filter_by(
                category_id=category_id).all()
    return jsonify(CategoryItem=[i.serialize for i in itemsList])


# Show all categories
@app.route('/')
@app.route('/catalog/', methods=['GET', 'POST'])
def showCategories():
    catalog = session.query(Category).order_by(asc(Category.id))
    itemsList = session.query(CategoryItem).filter_by(category_id=1).all()
    index = 1
    if 'username' not in login_session:
        return render_template('catalogPublic.html', categoryItems=itemsList,
                               catalog=catalog, index=index)
    else:
        return render_template('catalog.html', categoryItems=itemsList,
                               catalog=catalog, index=index)


# Show selected category and associated books
@app.route('/catalog/<int:category_id>/', methods=['GET', 'POST'])
def showItems(category_id):
    catalog = session.query(Category).order_by(asc(Category.id))
    itemsList = session.query(CategoryItem).filter_by(
                category_id=category_id).all()
    if 'username' not in login_session:
        return render_template('catalogPublic.html', categoryItems=itemsList,
                               catalog=catalog, index=category_id)
    else:
        return render_template('catalog.html', categoryItems=itemsList,
                               catalog=catalog, index=category_id)


# Show book description and details
@app.route('/catalog/<int:category_id>/book/<int:book_id>',
           methods=['GET', 'POST'])
def showDescription(category_id, book_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(CategoryItem).filter_by(id=book_id).one()
    if 'username' not in login_session:
        return render_template('descriptionPublic.html',
                               book=item, category=category)
    else:
        return render_template('description.html',
                               book=item, category=category)


# Create a new category
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        newCategory = Category(name=request.form['name'],
                               user_id=login_session['user_id'])
        session.add(newCategory)
        flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('addCategory.html')


# Edit a selected category
@app.route('/catalog/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')

    editedCategory = session.query(Category).filter_by(id=category_id).one()
    if editedCategory.user_id != login_session['user_id']:
        return ("<script>function myFunction() "
                "{ alert('You are not authorized to edit this category. "
                "You can only edit the category that you have created');"
                "setTimeout(function() {history.go(-1);}, 100);}"
                "</script><body onload='myFunction()''>")
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            flash('Category Successfully Edited %s' % editedCategory.name)
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('editCategory.html', category_id=category_id,
                               category_name=editedCategory.name)


# Delete category
@app.route('/catalog/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')

    selectedCategory = session.query(Category).filter_by(
                       id=category_id).first()
    if selectedCategory.user_id != login_session['user_id']:
        return ("<script>function myFunction() "
                "{ alert('You are not authorized to delete this category. "
                "You can only delete the category that you have created');"
                "setTimeout(function() {history.go(-1);}, 100);}"
                "</script><body onload='myFunction()''>")
    if request.method == 'POST':
        session.delete(selectedCategory)
        flash('%s Successfully Deleted' % selectedCategory.name)
        session.commit()
    return redirect(url_for('showCategories'))


# Add a new book
@app.route('/catalog/<int:category_id>/addbook/', methods=['GET', 'POST'])
def addBook(category_id):
    if 'username' not in login_session:
        return redirect('/login')

    selectedCategory = session.query(Category).filter_by(id=category_id).one()
    if selectedCategory.user_id != login_session['user_id']:
        return ("<script>function myFunction() " +
                "{ alert('You are not authorized to add a book to"
                " this category."
                "You can only add the book with category "
                "that you have created');"
                "setTimeout(function() {history.go(-1);}, 100);}"
                "</script><body onload='myFunction()''>")
    if request.method == 'POST':
        newBook = CategoryItem(name=request.form['name'],
                               author=request.form['author'],
                               description=request.form['description'],
                               category_id=category_id,
                               user_id=login_session['user_id'])
        session.add(newBook)
        session.commit()
        flash('New Book %s Successfully Created' % newBook.name)
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('addBook.html', category_id=category_id,
                               category_name=selectedCategory.name)


# Edit a book
@app.route('/catalog/<int:category_id>/book/<int:book_id>/edit',
           methods=['GET', 'POST'])
def editBook(category_id, book_id):
    if 'username' not in login_session:
        return redirect('/login')

    selectedCategory = session.query(Category).filter_by(id=category_id).one()
    book = session.query(CategoryItem).filter_by(id=book_id).one()
    if book.user_id != login_session['user_id']:
        return ("<script>function myFunction(){alert('You are not authorized "
                "to edit this book. You can only edit the book within category"
                " that you have created');setTimeout(function() "
                "{history.go(-1);}, 100);}"
                "</script><body onload='myFunction()''>")
    if request.method == 'POST':
        if request.form['name']:
            book.name = request.form['name']
        if request.form['author']:
            book.author = request.form['author']
        if request.form['description']:
            book.description = request.form['description']
        flash('Book %s Successfully Edited' % book.name)
        return render_template('description.html', book=book,
                               category=selectedCategory)
    else:
        return render_template('editBook.html', book=book,
                               category=selectedCategory)


# Delete a book
@app.route('/catalog/<int:category_id>/book/<int:book_id>/delete',
           methods=['GET', 'POST'])
def deleteBook(category_id, book_id):
    if 'username' not in login_session:
        return redirect('/login')

    selectedCategory = session.query(Category).filter_by(id=category_id).one()
    bookToDelete = session.query(CategoryItem).filter_by(id=book_id).one()
    if bookToDelete.user_id != login_session['user_id']:
        return ("<script>function myFunction() "
                "{ alert('You are not authorized to delete this book. "
                "You can only delete the book within category that you have "
                "created');"
                "setTimeout(function() {history.go(-1);}, 100);}"
                "</script><body onload='myFunction()''>")
    if request.method == 'POST':
        session.delete(bookToDelete)
        flash('Book %s Successfully Deleted' % bookToDelete.name)
        session.commit()
    return redirect(url_for('showItems', category_id=category_id))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
