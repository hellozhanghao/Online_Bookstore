#order order id
# order_1 = DB_Order('zhanghao',datetime.date.today(),'shipped')
# db.session.add(order_1)
# db.session.commit()
#
# detail_1 = DB_Order_Detail(order_1.order_id,'978-873625125',6)
# detail_2 = DB_Order_Detail(order_1.order_id,'978-873625125',7)
# db.session.add(detail_1)
# db.session.add(detail_2)
# db.session.commit()

# Example delete
# delete_this = DB_User.query.filter_by(username='zhanghao').first()
# db.session.delete(delete_this)
# db.session.commit()
#
# # orders detal involved in book A
# order_details_book_A = DB_Order_Detail.query.filter_by(ISBN=book_A.ISBN).all()
#
# # orders involved in book A
# orders_involved_in_book_A = set()
# for order_detail_book_A in order_details_book_A:
#     order = DB_Order.query.filter_by(order_id=order_detail_book_A.order_id).first()
#     if order not in orders_involved_in_book_A:
#         orders_involved_in_book_A.add(order)
#
# # users involved in book A
# user_book_A = set()
# for order in orders_involved_in_book_A:
#     user = DB_User.query.filter_by(username=order.username).first()
#     if user not in user_book_A:
#         user_book_A.add(user)
#
# # orders detal involved in book B
# order_details_book_B = DB_Order_Detail.query.filter_by(ISBN=book_B.ISBN).all()
#
# # orders involved in book B
# orders_involved_in_book_B = set()
# for order_detail_book_B in order_details_book_B:
#     order = DB_Order.query.filter_by(order_id=order_detail_book_B.order_id).first()
#     if order not in orders_involved_in_book_B:
#         orders_involved_in_book_B.add(order)
#
# # users involved in book A
# user_book_B = set()
# for order in orders_involved_in_book_B:
#     user = DB_User.query.filter_by(username=order.username).first()
#     if user not in user_book_B:
#         user_book_B.add(user)


