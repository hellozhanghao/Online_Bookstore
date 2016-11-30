# import pymysql
#
#
# connection = pymysql.connect(host='localhost', port=3306, user='root', passwd='zhanghao', db='book_store')
#
# cursor = connection.cursor()
# try:
#     cursor.execute("SELECT * FROM USER ")
#     for row in cursor:
#         print(row)
# except:
#     print("Error")
#
# print()
#
#
# cursor.close()
# connection.close()


from book_store import DB_User
from book_store import db

user=DB_User('someone','password')
db.session.add(user)
db.session.commit()