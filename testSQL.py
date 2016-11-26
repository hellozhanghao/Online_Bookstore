import pymysql

# conn = pymysql.connect(host='10.13.32.40', port=3306, user='root', passwd='zhanghao', db='test')

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='zhanghao', db='test')

cur = conn.cursor()
try:
    cur.execute("CREATE TABLE test_table(line INT)")
except:
    print("Error")

print()


cur.close()
conn.close()