from flask import Flask, url_for, request, json, jsonify, render_template
import flask_login
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
from calendar import monthrange

from flask_table import Table, Col, ButtonCol

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zhanghao@localhost/book_store'
db = SQLAlchemy(app)


# ***********************************************************************************
# ------------------------------------DB schemas------------------------------------
# ***********************************************************************************
class DB_User(db.Model):
    __tablename__ = 'User'
    username = db.Column('username', db.CHAR(100), primary_key=True)
    password = db.Column('password', db.CHAR(100))
    credit_card = db.Column('credit_card', db.CHAR(100))
    address = db.Column('address', db.CHAR(100))
    phone = db.Column('phone', db.CHAR(100))
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
    ISBN = db.Column('ISBN', db.CHAR(100), primary_key=True)
    title = db.Column('title', db.CHAR(100))
    author = db.Column('author', db.CHAR(100))
    publisher = db.Column('publisher', db.CHAR(100))
    year = db.Column('year', db.INTEGER)
    copy = db.Column('copy', db.INTEGER)
    price = db.Column('price', db.FLOAT)
    format = db.Column('format', db.CHAR(100))
    subject = db.Column('subject', db.CHAR(100))
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
    username = db.Column('username', db.ForeignKey('User.username'))
    ISBN = db.Column('ISBN', db.ForeignKey('Book.ISBN'))
    quantity = db.Column('quantity', db.INTEGER)

    def __init__(self, username, ISBN, quantity):
        self.username = username
        self.ISBN = ISBN
        self.quantity = quantity


class DB_Review(db.Model):
    __tablename__ = "Review"
    review_id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column('username', db.ForeignKey('User.username'))
    ISBN = db.Column('ISBN', db.ForeignKey('Book.ISBN'))
    score = db.Column('score', db.INTEGER)
    text = db.Column('text', db.CHAR(100))
    date = db.Column('date', db.DATE)

    def __init__(self, username, ISBN, score, text, date):
        self.username = username
        self.ISBN = ISBN
        self.score = score
        self.text = text
        self.date = date


class DB_Comment(db.Model):
    __tablename__ = "Comment"
    comment_id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column('username', db.ForeignKey('User.username'))
    review_id = db.Column('review_id', db.ForeignKey('Review.review_id'))
    usefulness = db.Column('usefulness', db.CHAR(100))

    def __init__(self, username, review_id, usefulness):
        self.username = username
        self.review_id = review_id
        self.usefulness = usefulness


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
    score = Col('Score')
    detial = ButtonCol('View Details', 'search', url_kwargs=dict(ISBN='ISBN'))


class BookItem(object):
    def __init__(self, ISBN, title, author, publisher, year, price, score):
        self.ISBN = ISBN
        self.title = title
        self.author = author
        self.publisher = publisher
        self.year = year
        self.price = price
        self.score = score


class TopItemTable(Table):
    name = Col('')
    description = Col('Qty')


class TopItem(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description


class ReviewTable(Table):
    review_id = Col('Review ID')
    user = Col('User')
    text = Col('Description')
    score = Col('Review Score')
    date = Col('Date Reviewed')
    usefulness = Col('Usefulness')
    comment = ButtonCol('Comment', 'comment', url_kwargs=dict(review_id='review_id'))


class ReviewItem(object):
    def __init__(self, review_id, user, text, score, date, usefulness):
        self.review_id = review_id
        self.user = user
        self.text = text
        self.score = score
        self.usefulness = usefulness
        self.date = date


class MYReviewTable(Table):
    title = Col('Title')
    text = Col('Description')
    score = Col('Score')
    date = Col('Date')
    veryuseful = Col('Very Useful')
    useful = Col('Useful')
    useless = Col('Useless')
    usefulness = Col('Usefulness score')


class MYReviewItem(object):
    def __init__(self, title, text, score, date, veryuseful, useful, useless, usefulness):
        self.title = title
        self.text = text
        self.score = score
        self.veryuseful = veryuseful
        self.useful = useful
        self.useless = useless
        self.date = date
        self.usefulness = usefulness


class MYCommentTable(Table):
    title = Col('Title')
    text = Col('Description')
    by = Col('By')
    score = Col('Score')
    mycomment = Col('My Comment')


class MYCommentItem(object):
    def __init__(self, title, text, by, score, mycomment):
        self.title = title
        self.text = text
        self.by = by
        self.score = score
        self.mycomment = mycomment


# ***********************************************************************************
# ------------------------------------Flask------------------------------------------
# ***********************************************************************************



@app.route('/')
@flask_login.login_required
def index():
    # get books user purchased
    orders = DB_Order.query.filter_by(username=flask_login.current_user.id).all()
    book_purchased = set()
    for order in orders:
        order_details = DB_Order_Detail.query.filter_by(order_id=order.order_id).all()
        for order_detail in order_details:
            book = DB_Book.query.filter_by(ISBN=order_detail.ISBN).first()
            if book not in book_purchased:
                book_purchased.add(book)

    # get my orders
    my_orders = set()
    for order in orders:
        my_orders.add(order)

    # get related orders
    order_related = set()
    for book in book_purchased:
        order_details_related_to_book = DB_Order_Detail.query.filter_by(ISBN=book.ISBN).all()
        for order_detail in order_details_related_to_book:
            order = DB_Order.query.filter_by(order_id=order_detail.order_id).first()
            if (order not in order_related) and (order not in my_orders):
                order_related.add(order)

    # map related order to related user
    related_users = set()
    for order in order_related:
        user = DB_User.query.filter_by(username=order.username).first()
        if user not in related_users:
            related_users.add(user)

    # get book purchased by others
    book_purchased_by_others = set()
    for user in related_users:
        orders = DB_Order.query.filter_by(username=user.username).all()
        for order in orders:
            order_details = DB_Order_Detail.query.filter_by(order_id=order.order_id).all()
            for order_detail in order_details:
                book = DB_Book.query.filter_by(ISBN=order_detail.ISBN).first()
                if book not in book_purchased_by_others:
                    book_purchased_by_others.add(book)

    # get recommended books
    recommended_books = []
    for book in book_purchased_by_others:
        if book not in book_purchased:
            recommended_books.append(book)

    # order recommended books
    count_books = {}
    for book in recommended_books:
        count_books[book] = 0

    for user in related_users:
        for book_A in book_purchased:

            user_purchased_book_A = False
            orders = DB_Order.query.filter_by(username=user.username).all()
            for order in orders:
                order_details = DB_Order_Detail.query.filter_by(order_id=order.order_id, ISBN=book_A.ISBN).all()
                if order_details is not None:
                    user_purchased_book_A = True

            if user_purchased_book_A:
                for book_B in recommended_books:
                    for order in orders:
                        order_details = DB_Order_Detail.query.filter_by(order_id=order.order_id, ISBN=book_B.ISBN).all()

                        for order_detail in order_details:
                            book = DB_Book.query.filter_by(ISBN=order_detail.ISBN).first()
                            count_books[book] += order_detail.quantity

    inv_map = {v: k for k, v in count_books.items()}

    ordered_books = []
    for item in sorted(inv_map):
        # print(inv_map[item].ISBN,item)
        ordered_books.append(inv_map[item])

    ordered_books.reverse()

    # generate table
    book_recommentation = []
    for book in ordered_books:
        # todo add score
        avg_score = 0.0
        reviews = DB_Review.query.filter_by(ISBN=book.ISBN).all()
        for review in reviews:
            avg_score += review.score

        if len(reviews)!= 0:
            avg_score /= len(reviews)

        book_recommentation.append(
            BookItem(book.ISBN, book.title, book.author, book.publisher, book.year, book.price, avg_score))

    book_recommentation_table = BookTable(book_recommentation)

    return render_template('index.html', username=flask_login.current_user.id,
                           book_recommentation_table=book_recommentation_table)


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
    return render_template('generic.html', msg="Bad Login")


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

    return render_template('generic.html', msg='Bad Sign Up! Username exist')


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
    total_qty = 0
    total_price = 0.0
    for cart in carts:
        book = DB_Book.query.filter_by(ISBN=cart.ISBN).first()
        cart_info.append(CartItem(cart.ISBN, book.title, cart.quantity))
        total_qty += cart.quantity
        total_price += float(book.price) * cart.quantity

    cart_info_table = CartTable(cart_info)

    return render_template('account_cart.html', cart_info_table=cart_info_table,
                           total_qty=total_qty, total_price=round(total_price, 2))


@app.route('/account/checkout')
@flask_login.login_required
def checkout():
    # check availability
    cart_items = DB_Shopping_Cart.query.filter_by(username=flask_login.current_user.id).all()
    for cart_item in cart_items:
        book_item = DB_Book.query.filter_by(ISBN=cart_item.ISBN).first()
        if book_item.copy < cart_item.quantity:
            return "No enough stock for " + book_item.title

    # update inventory
    for cart_item in cart_items:
        book_item = DB_Book.query.filter_by(ISBN=cart_item.ISBN).first()
        book_item.copy -= cart_item.quantity
        db.session.commit()

    # create order
    new_order = DB_Order(flask_login.current_user.id, datetime.date.today(), 'Shipped')
    db.session.add(new_order)
    db.session.commit()

    # create order items
    for cart_item in cart_items:
        book_item = DB_Book.query.filter_by(ISBN=cart_item.ISBN).first()
        new_order_detail = DB_Order_Detail(new_order.order_id, book_item.ISBN, cart_item.quantity)
        db.session.add(new_order_detail)
        db.session.commit()

    # update shopping cart
    cart_items = DB_Shopping_Cart.query.filter_by(username=flask_login.current_user.id).all()
    for cart_item in cart_items:
        db.session.delete(cart_item)
        db.session.commit()
    return redirect(url_for('order'))


@app.route('/account/reviews')
@flask_login.login_required
def reviews():
    review_info = []
    reviews = DB_Review.query.filter_by(username=flask_login.current_user.id).all()

    for review in reviews:
        book = DB_Book.query.filter_by(ISBN=review.ISBN).first()

        veryuseful = 0
        useful = 0
        useless = 0

        comments = DB_Comment.query.filter_by(review_id=review.review_id).all()
        for comment in comments:
            if comment.usefulness == 'very useful':
                veryuseful += 1
            if comment.usefulness == 'useful':
                useful += 1
            if comment.usefulness == 'useless':
                useless += 1

        usefulness = (veryuseful * 2.0 + useful * 1.0) / len(comments)

        review_info.append(MYReviewItem(book.title,
                                        review.text,
                                        review.score,
                                        review.date,
                                        veryuseful,
                                        useful,
                                        useless, usefulness))

    review_info_table = MYReviewTable(review_info)
    return render_template('account_reviews.html', review_info_table=review_info_table)


@app.route('/account/comment')
@flask_login.login_required
def my_comments():
    comments_info = []

    comments = DB_Comment.query.filter_by(username=flask_login.current_user.id).all()
    for comment in comments:
        review = DB_Review.query.filter_by(review_id=comment.review_id).first()
        book = DB_Book.query.filter_by(ISBN=review.ISBN).first()
        comments_info.append(MYCommentItem(book.title,
                                           review.text,
                                           review.username,
                                           review.score,
                                           comment.usefulness))

    comments_info_table = MYCommentTable(comments_info)

    return render_template('account_comments.html', comments_info_table=comments_info_table)


# ******************************* Admin Pages ***************************************

@app.route('/admin')
@flask_login.login_required
def admin():
    db_user = DB_User.query.filter_by(username=flask_login.current_user.id).first()
    if db_user.admin:
        return render_template('admin.html', username=flask_login.current_user.id)
    return render_template('generic.html', msg="Access denied!")


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

        return render_template('generic.html', msg="Access denied!")

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
    # if request.method == 'POST':
    #     return render_template('admin_inventory_add.html', ISBN=ISBN)
    db_user = DB_User.query.filter_by(username=flask_login.current_user.id).first()
    if db_user.admin:
        return render_template('admin_inventory_add.html', ISBN=ISBN)
    return render_template('generic.html', msg='access denied!')


@app.route('/admin/inventory/add/number', methods=['GET', 'POST'])
@flask_login.login_required
def number():
    db_user = DB_User.query.filter_by(username=flask_login.current_user.id).first()
    if db_user.admin:
        if request.method == 'POST':
            ISBN = request.form['ISBN']
            number = request.form['number']
            number = int(number)
            db_book = DB_Book.query.filter_by(ISBN=ISBN).first()
            db_book.copy += number
            db.session.commit()
        return redirect(url_for('inventory'))
    return render_template('generic.html', msg='Access denied!')


@app.route('/admin/statistics', methods=['GET', 'POST'])
@flask_login.login_required
def statistics():
    db_user = DB_User.query.filter_by(username=flask_login.current_user.id).first()
    if db_user.admin:
        if request.method == 'GET':
            return render_template('admin_statistics.html')
        if request.method == 'POST':
            m = int(request.form['m'])
            current_year = datetime.date.today().year
            current_month = datetime.date.today().month
            days = []
            for i in range(1, monthrange(current_year, current_month)[1] + 1):
                days.append(i)

            dates_in_current_month = []
            for day in days:
                dates_in_current_month.append(datetime.date(current_year, current_month, day))

            all_orders_this_month = set()
            for date in dates_in_current_month:
                orders_on_date = DB_Order.query.filter_by(date=date).all()
                for order_on_date in orders_on_date:
                    all_orders_this_month.add(order_on_date)

            # book mapping
            popular_books = {}
            for order in all_orders_this_month:
                order_details = DB_Order_Detail.query.filter_by(order_id=order.order_id).all()
                for order_detail in order_details:
                    book = DB_Book.query.filter_by(ISBN=order_detail.ISBN).first()
                    if book not in popular_books:
                        popular_books[book] = order_detail.quantity
                    else:
                        popular_books[book] += order_detail.quantity

            sorted_books = sorted(popular_books, key=popular_books.get, reverse=True)

            if len(sorted_books) < m:
                m_sorted_books = sorted_books
            else:
                m_sorted_books = sorted_books[:m]

            book_info = []
            for book in m_sorted_books:
                book_info.append(TopItem(book.title, popular_books[book]))
            book_info_table = TopItemTable(book_info)

            # author mapping
            popular_authors = {}
            for order in all_orders_this_month:
                order_details = DB_Order_Detail.query.filter_by(order_id=order.order_id).all()
                for order_detail in order_details:
                    book = DB_Book.query.filter_by(ISBN=order_detail.ISBN).first()
                    if book.author not in popular_authors:
                        popular_authors[book.author] = order_detail.quantity
                    else:
                        popular_authors[book.author] += order_detail.quantity

            sorted_authors = sorted(popular_authors, key=popular_authors.get, reverse=True)

            if len(sorted_authors) < m:
                m_sorted_authors = sorted_authors
            else:
                m_sorted_authors = sorted_authors[:m]

            author_info = []
            for author in m_sorted_authors:
                author_info.append(TopItem(author, popular_authors[author]))
            author_info_table = TopItemTable(author_info)

            # publisher mapping
            popular_publishers = {}
            for order in all_orders_this_month:
                order_details = DB_Order_Detail.query.filter_by(order_id=order.order_id).all()
                for order_detail in order_details:
                    book = DB_Book.query.filter_by(ISBN=order_detail.ISBN).first()
                    if book.publisher not in popular_publishers:
                        popular_publishers[book.publisher] = order_detail.quantity
                    else:
                        popular_publishers[book.publisher] += order_detail.quantity

            sorted_publishers = sorted(popular_publishers, key=popular_publishers.get, reverse=True)

            if len(sorted_publishers) < m:
                m_sorted_publishers = sorted_publishers
            else:
                m_sorted_publishers = sorted_publishers[:m]

            publisher_info = []
            for publisher in m_sorted_publishers:
                publisher_info.append(TopItem(publisher, popular_publishers[publisher]))
            publisher_info_table = TopItemTable(publisher_info)

            return render_template('admin_statistics_view.html',
                                   m=m,
                                   current_year=current_year,
                                   current_month=current_month,
                                   book_info_table=book_info_table,
                                   author_info_table=author_info_table,
                                   publisher_info_table=publisher_info_table)
    return render_template('generic.html', msg='access denied!')


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
                books_by_title = DB_Book.query.filter(DB_Book.title.contains(title)).all()
                input.append(books_by_title)
            if author != "":
                books_by_author = DB_Book.query.filter(DB_Book.author.contains(author)).all()
                input.append(books_by_author)
            if publisher != "":
                books_by_publisher = DB_Book.query.filter(DB_Book.publisher.contains(publisher)).all()
                input.append(books_by_publisher)
            if books_by_subject != "":
                books_by_subject = DB_Book.query.filter(DB_Book.subject.contains(subject)).all()
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
                book_dict={}
                for book in books:
                    avg_score = 0.0
                    reviews = DB_Review.query.filter_by(ISBN=book.ISBN).all()
                    for review in reviews:
                        avg_score += review.score

                    if len(reviews) != 0:
                        avg_score /= len(reviews)

                    book_dict[book] = avg_score

                if order =='increasing':
                    books = sorted(book_dict, key=book_dict.get)
                else:
                    books = sorted(book_dict, key=book_dict.get,reverse=True)

            book_info = []
            for book in books:
                # todo add score

                avg_score = 0.0
                reviews = DB_Review.query.filter_by(ISBN=book.ISBN).all()
                for review in reviews:
                    avg_score += review.score

                if len(reviews) != 0:
                    avg_score /= len(reviews)

                book_info.append(BookItem(book.ISBN,
                                          book.title,
                                          book.author,
                                          book.publisher,
                                          book.year,
                                          book.price,
                                          avg_score))

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

    book_exist = False

    all_cart_records = DB_Shopping_Cart.query.filter_by(username=flask_login.current_user.id).all()
    for record in all_cart_records:
        if record.ISBN == request.form['ISBN']:
            book_exist = True
    if book_exist:
        print("Exist")
        cart_record = DB_Shopping_Cart.query.filter_by(username=flask_login.current_user.id,
                                                       ISBN=request.form['ISBN']).first()
        print(cart_record.quantity)
        cart_record.quantity += copy
        db.session.commit()
        print(cart_record.quantity)

    else:
        new_cart_record = DB_Shopping_Cart(flask_login.current_user.id, request.form['ISBN'], copy)
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


# ******************************* Review and Comment ***********************************
@app.route('/review', methods=['GET', 'POST'])
@flask_login.login_required
def review():
    ISBN = request.form['ISBN']

    previous_review = DB_Review.query.filter_by(username=flask_login.current_user.id, ISBN=ISBN).first()
    if previous_review is not None:
        return "You have previously reviewed this book! "

    # check if user bought this book
    purchased = False
    orders = DB_Order.query.filter_by(username=flask_login.current_user.id).all()
    for order in orders:
        order_details = DB_Order_Detail.query.filter_by(order_id=order.order_id).all()
        for order_detail in order_details:
            if ISBN == order_detail.ISBN:
                purchased = True
                break

    if not purchased:
        return "You need to purchase this book before review"

    score = request.form['score']
    text = request.form['review']
    new_review = DB_Review(flask_login.current_user.id, ISBN, score, text, datetime.date.today())
    db.session.add(new_review)
    db.session.commit()

    return redirect(url_for('detail', ISBN=ISBN))


@app.route('/review_detail', methods=['GET', 'POST'])
@flask_login.login_required
def review_detail():
    ISBN = request.form['ISBN']
    n = request.form['number']
    review_info = []
    reviews = DB_Review.query.filter_by(ISBN=ISBN).all()

    avg_score = {}
    for review in reviews:
        veryuseful = 0
        useful = 0
        useless = 0

        comments = DB_Comment.query.filter_by(review_id=review.review_id).all()

        for comment in comments:
            if comment.usefulness == 'very useful':
                veryuseful += 1
            if comment.usefulness == 'useful':
                useful += 1
            if comment.usefulness == 'useless':
                useless += 1

        if len(comments) != 0:
            usefulness = (veryuseful * 2.0 + useful * 1.0) / len(comments)
        else:
            usefulness = 0.0

        avg_score[review] = usefulness

    sorted_avg_score = sorted(avg_score, key=avg_score.get, reverse=True)
    if n == '':
        n = len(sorted_avg_score)
    else:
        n = int(n)
    if len(sorted_avg_score) < n:
        n = len(sorted_avg_score)
    for i in range(n):
        review_info.append(ReviewItem(sorted_avg_score[i].review_id,
                                      sorted_avg_score[i].username,
                                      sorted_avg_score[i].text,
                                      sorted_avg_score[i].score,
                                      sorted_avg_score[i].date,
                                      avg_score[sorted_avg_score[i]]))

    review_info_table = ReviewTable(review_info)
    return render_template('review_detail.html', review_info_table=review_info_table, n=n)


@app.route('/comment', methods=['GET', 'POST'])
@flask_login.login_required
def comment():
    review_id = request.args['review_id']
    review = DB_Review.query.filter_by(review_id=review_id).first()
    book = DB_Book.query.filter_by(ISBN=review.ISBN).first()

    if review.username == flask_login.current_user.id:
        return "You can't comment on your own review"

    return render_template('comment.html', review_id=review_id, book_title=book.title, ISBN=book.ISBN)


@app.route('/comment/post', methods=['GET', 'POST'])
@flask_login.login_required
def post_comment():
    username = flask_login.current_user.id
    review_id = request.form['review_id']
    usefulness = request.form['usefulness']

    comment = DB_Comment.query.filter_by(username=username, review_id=review_id).first()
    if comment is not None:
        return "You already commented on this review"

    comment = DB_Comment(username, review_id, usefulness)
    db.session.add(comment)
    db.session.commit()

    return redirect(url_for('detail', ISBN=request.form['ISBN']))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
