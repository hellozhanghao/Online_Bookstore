from flask import Flask, url_for, request, json, jsonify, render_template
import flask_login
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

from flask_table import Table, Col, ButtonCol

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zhanghao@localhost/book_store'
db = SQLAlchemy(app)


# ***********************************************************************************
# ------------------------------------DB schemas------------------------------------
# ***********************************************************************************
class DB_User(db.Model):
    __tablename__ = 'User'
    username = db.Column('username', db.CHAR(20), primary_key=True)
    password = db.Column('password', db.CHAR(20))
    credit_card = db.Column('credit_card', db.CHAR(20))
    address = db.Column('address', db.CHAR(20))
    phone = db.Column('phone', db.CHAR(20))
    admin = db.Column('admin', db.BOOLEAN)

    def __init__(self, username, password, credit_card, address, phone, admin):
        self.username = username
        self.password = password
        self.credit_card = credit_card
        self.address = address
        self.phone = phone
        self.admin = admin


class DB_Book(db.Model):
    __tablename__ = "Book"
    ISBN = db.Column('ISBN', db.CHAR(14), primary_key=True)
    title = db.Column('title', db.CHAR(40))
    author = db.Column('author', db.CHAR(40))
    publisher = db.Column('publisher', db.CHAR(40))
    year = db.Column('year', db.INTEGER)
    copy = db.Column('copy', db.INTEGER)
    price = db.Column('price', db.FLOAT)
    format = db.Column('format', db.CHAR(20))
    subject = db.Column('subject', db.CHAR(20))
    keywords = db.Column('keywords', db.CHAR(100))

    def __init__(self, ISBN, title, author, publisher, year, copy, price, format, subject, keywords):
        self.ISBN = ISBN
        self.title = title
        self.author = author
        self.publisher = publisher
        self.year = year
        self.copy = copy
        self.price = price
        self.format = format
        self.subject = subject
        self.keywords = keywords


class DB_Order(db.Model):
    __tablename__ = 'Orders'
    order_id = db.Column('order_id', db.INTEGER, primary_key=True)
    username = db.Column('username', db.ForeignKey('User.username'), )
    date = db.Column('date', db.DATE)
    status = db.Column('status', db.CHAR(30))

    # orders = db.relationship('DB_Order_Detail', backref='user', lazy='dynamic')

    def __init__(self, username, date, status):
        self.username = username
        self.date = date
        self.status = status


class DB_Order_Detail(db.Model):
    __tablename__ = "Order_Detail"
    order_detail_id = db.Column(db.INTEGER, primary_key=True)
    order_id = db.Column('order_id', db.ForeignKey('Orders.order_id'))
    ISBN = db.Column('ISBN', db.ForeignKey('Book.ISBN'))
    quantity = db.Column('quantity', db.INTEGER)

    def __init__(self, order_id, ISBN, quantity):
        self.order_id = order_id
        self.ISBN = ISBN
        self.quantity = quantity


class DB_Shopping_Cart(db.Model):
    __tablename__ = "Shopping_Cart"
    cart_item_id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column('username', db.ForeignKey('User.username'), )
    ISBN = db.Column('ISBN', db.ForeignKey('Book.ISBN'))
    quantity = db.Column('quantity', db.INTEGER)

    def __init__(self, username, ISBN, quantity):
        self.username = username
        self.ISBN = ISBN
        self.quantity = quantity


db.create_all()
db.session.commit()

# ***********************************************************************************
# ------------------------------------Login Manager----------------------------------
# ***********************************************************************************

app.secret_key = 'super secret string'  # todo Change this

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    db_user = DB_User.query.filter_by(username=username).first()
    if db_user is None:
        return
    user = User()
    user.id = username
    return user


# @login_manager.request_loader
# def request_loader(request):
#     print("call")
#     email = request.form.get('email')
#     if email not in users:
#         return
#
#     user = User()
#     user.id = email
#
#     # DO NOT ever store passwords in plaintext and always compare password
#     # hashes using constant-time comparison!
#     user.is_authenticated = request.form['pw'] == users[email]['pw']
#
#     return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))


# ***********************************************************************************
# ------------------------------------Flask Table------------------------------------
# ***********************************************************************************

class ItemTable(Table):
    name = Col('Name')
    description = Col('Description')


class Item(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description


class OrderTable(Table):
    order_id = Col('Order ID')
    date = Col('Date Ordered')
    status = Col('Order Status')
    book = Col('Book Name')
    qty = Col('Quantity')


class OrderItem(object):
    def __init__(self, order_id, date, status, book, qty):
        self.order_id = order_id
        self.date = date
        self.status = status
        self.book = book
        self.qty = qty


class CartTable(Table):
    ISBN = Col('ISBN')
    book = Col('Book Name')
    qty = Col('Quantity')


class CartItem(object):
    def __init__(self, ISBN, book, qty):
        self.ISBN = ISBN
        self.book = book
        self.qty = qty


class InventoryTable(Table):
    ISBN = Col('ISBN')
    title = Col('Title')
    author = Col('Author')
    publisher = Col('Publisher')
    year = Col('Year')
    copy = Col('Copy')
    price = Col('Price')
    format_1 = Col('Format')
    subject = Col('Subject')
    add = ButtonCol('Add', 'add', url_kwargs=dict(ISBN='ISBN'))


class InventoryItem(object):
    def __init__(self, ISBN, title, author, publisher, year, copy, price, format_1, subject):
        self.ISBN = ISBN
        self.title = title
        self.author = author
        self.publisher = publisher
        self.year = year
        self.copy = copy
        self.price = price
        self.format_1 = format_1
        self.subject = subject


class BookTable(Table):
    ISBN = Col('ISBN')
    title = Col('Title')
    author = Col('Author')
    publisher = Col('Publisher')
    year = Col('Year')
    price = Col('Price')
    # add = ButtonCol('Add To Cart', 'cart', url_kwargs=dict(ISBN='ISBN'))
    detial = ButtonCol('View Details', 'search', url_kwargs=dict(ISBN='ISBN'))


class BookItem(object):
    def __init__(self, ISBN, title, author, publisher, year, price, ):
        self.ISBN = ISBN
        self.title = title
        self.author = author
        self.publisher = publisher
        self.year = year
        self.price = price


# ***********************************************************************************
# ------------------------------------Flask------------------------------------------
# ***********************************************************************************



@app.route('/')
@flask_login.login_required
def index():
    return render_template('index.html', username=flask_login.current_user.id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if flask_login.current_user.is_authenticated:
            return redirect(url_for('index'))
        else:
            return render_template('login.html')

    if request.method == 'POST':
        username = request.form['username']
        db_user = DB_User.query.filter_by(username=username).first()
        if db_user is not None:
            if request.form['password'] == db_user.password:
                user = User()
                user.id = username
                flask_login.login_user(user)
                return redirect(url_for('index'))
    return 'Bad login'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        username = request.form['username']
        db_user = DB_User.query.filter_by(username=username).first()
        if db_user is None:
            new_user = DB_User(username,
                               request.form['password'],
                               request.form['credit_card'],
                               request.form['address'],
                               request.form['phone'],
                               False)
            db.session.add(new_user)
            db.session.commit()

            user = User()
            user.id = username
            flask_login.login_user(user)
            return redirect(url_for('index'))

    return 'Bad Sign Up! Username exist'


@app.route('/logout')
@flask_login.login_required
def logout():
    username = flask_login.current_user.id
    flask_login.logout_user()
    return render_template('logout.html', username=username)


# ******************************* Account Pages ***************************************


@app.route('/account')
@flask_login.login_required
def profile():
    return render_template('account.html')


@app.route('/account/profile')
@flask_login.login_required
def account():
    # Account Info
    db_user = DB_User.query.filter_by(username=flask_login.current_user.id).first()
    account_info = [Item('Username', db_user.username),
                    Item('Credit Card', db_user.credit_card),
                    Item('Address', db_user.address),
                    Item('Phone', db_user.phone)]

    account_info_table = ItemTable(account_info)
    return render_template('account_profile.html',
                           account_info_table=account_info_table)


@app.route('/account/order')
@flask_login.login_required
def order():
    # Order Details
    order_info = []
    orders = DB_Order.query.filter_by(username=flask_login.current_user.id).all()
    for order in orders:
        books = DB_Order_Detail.query.filter_by(order_id=order.order_id).all()
        entry = 0
        for book in books:
            order_id = order.order_id
            date = order.date
            status = order.status
            book_record = DB_Book.query.filter_by(ISBN=book.ISBN).first()
            bookname = book_record.title
            qty = book.quantity
            if entry == 0:
                order_info.append(OrderItem(order_id, date, status, bookname, qty))
            else:
                order_info.append(OrderItem('', '', '', bookname, qty))
            entry += 1

    order_info_table = OrderTable(order_info)
    return render_template('account_order.html', order_info_table=order_info_table)


@app.route('/account/cart')
@flask_login.login_required
def cart():
    # cart detail
    cart_info = []

    carts = DB_Shopping_Cart.query.filter_by(username=flask_login.current_user.id).all()
    for cart in carts:
        book = DB_Book.query.filter_by(ISBN=cart.ISBN).first()
        cart_info.append(CartItem(cart.ISBN, book.title, cart.quantity))

    cart_info_table = CartTable(cart_info)

    return render_template('account_cart.html', cart_info_table=cart_info_table)


# ******************************* Admin Pages ***************************************

@app.route('/admin')
@flask_login.login_required
def admin():
    db_user = DB_User.query.filter_by(username=flask_login.current_user.id).first()
    if db_user.admin:
        return render_template('admin.html', username=flask_login.current_user.id)
    return "Access denied! Only admin can view this page"


@app.route('/admin/inventory', methods=['GET', 'POST'])
@flask_login.login_required
def inventory():
    if request.method == 'GET':
        db_user = DB_User.query.filter_by(username=flask_login.current_user.id).first()
        if db_user.admin:
            inventory_info = []
            books = DB_Book.query.filter_by().all()
            for book in books:
                inventory_info.append(InventoryItem(book.ISBN,
                                                    book.title,
                                                    book.author,
                                                    book.publisher,
                                                    book.year,
                                                    book.copy,
                                                    book.price,
                                                    book.format,
                                                    book.subject))
            inventory_info_table = InventoryTable(inventory_info)
            return render_template('admin_inventory.html', inventory_info_table=inventory_info_table)

        return "Access denied! Only admin can view this page"

    if request.method == 'POST':
        ISBN = request.form['ISBN']
        db_book = DB_Book.query.filter_by(ISBN=ISBN).first()
        if db_book is not None:
            return "Book exist"
        else:
            new_book = DB_Book(ISBN,
                               request.form['title'],
                               request.form['author'],
                               request.form['publisher'],
                               request.form['year'],
                               request.form['copy'],
                               request.form['price'],
                               request.form['format'],
                               request.form['subject'],
                               request.form['keywords'])
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('inventory'))


@app.route('/admin/inventory/add/<ISBN>', methods=['GET', 'POST'])
@flask_login.login_required
def add(ISBN):
    if request.method == 'POST':
        return render_template('admin_inventory_add.html', ISBN=ISBN)


@app.route('/admin/inventory/add/number', methods=['GET', 'POST'])
@flask_login.login_required
def number():
    if request.method == 'POST':
        ISBN = request.form['ISBN']
        number = request.form['number']
        number = int(number)
        db_book = DB_Book.query.filter_by(ISBN=ISBN).first()
        db_book.copy += number
        db.session.commit()
    return redirect(url_for('inventory'))


@app.route('/admin/statistics')
@flask_login.login_required
def statistics():
    return render_template('admin_statistics.html')



# ******************************* Shopping ^_^ ***************************************


@app.route('/search', methods=['GET', 'POST'])
@flask_login.login_required
def search():
    if request.method == 'POST':
        if dict(request.args) == {}:
            title = request.form['title']
            author = request.form['author']
            publisher = request.form['publisher']
            subject = request.form['subject']
            condition = request.form['condition']
            sort_by = request.form['sort_by']
            order = request.form['order']

            books_by_title = []
            books_by_author = []
            books_by_publisher = []
            books_by_subject = []
            input = []

            if title != "":
                books_by_title = DB_Book.query.filter_by(title=title).all()
                input.append(books_by_title)
            if author != "":
                books_by_author = DB_Book.query.filter_by(author=author).all()
                input.append(books_by_author)
            if publisher != "":
                books_by_publisher = DB_Book.query.filter_by(publisher=publisher).all()
                input.append(books_by_publisher)
            if books_by_subject != "":
                books_by_subject = DB_Book.query.filter_by(subject=subject).all()
                input.append(books_by_subject)

            if condition == "and":
                if len(input) == 0:
                    books_set = set()
                else:
                    books_set = set(input[0])
                    index = 1
                    while index < len(input):
                        books_set.intersection(input[index])
                        index += 1
            else:
                books_set = set(books_by_title).union(books_by_author) \
                    .union(books_by_publisher) \
                    .union(books_by_subject)

            books = []
            for book in books_set:
                books.append(book)

            if sort_by == 'year':
                if order == 'increasing':
                    books.sort(key=lambda x: x.year)
                else:
                    books.sort(key=lambda x: x.year, reverse=True)
            else:
                # todo add score
                print()

            book_info = []
            for book in books:
                book_info.append(BookItem(book.ISBN,
                                          book.title,
                                          book.author,
                                          book.publisher,
                                          book.year,
                                          book.price))

            book_info_table = BookTable(book_info)
            return render_template('search.html', book_info_table=book_info_table)
        else:
            return redirect(url_for('detail', ISBN=request.args['ISBN']))


@app.route('/detail/addtocart', methods=['GET', 'POST'])
@flask_login.login_required
def addtocart():
    copy = int(request.form['copy'])

    # load user
    db_user = DB_User.query.filter_by(username=flask_login.current_user.id).first()

    # load Book
    book_record = DB_Book.query.filter_by(ISBN=request.form['ISBN']).first()
    if copy > book_record.copy:
        return "Not enough stock!"

    new_cart_record = DB_Shopping_Cart(flask_login.current_user.id,request.form['ISBN'],copy)
    db.session.add(new_cart_record)
    db.session.commit()
    return redirect(url_for('cart'))


@app.route('/detail/<ISBN>', methods=['GET', 'POST'])
@flask_login.login_required
def detail(ISBN):
    book = DB_Book.query.filter_by(ISBN=ISBN).first()

    info = []
    info.append(Item("Titile", book.title))
    info.append(Item("ISBN", book.ISBN))
    info.append(Item("Author", book.author))
    info.append(Item("Publisher", book.publisher))
    info.append(Item("Year", book.year))
    info.append(Item("Copy in stock", book.copy))
    info.append(Item("Price", book.price))
    info.append(Item("Format", book.format))
    info.append(Item("Subject", book.subject))
    info.append(Item("Key Words", book.keywords))

    info_table = ItemTable(info)

    return render_template('detail.html', title=book.title, ISBN=ISBN,
                           author=book.author, info_table=info_table)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
