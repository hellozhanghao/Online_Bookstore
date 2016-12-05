create database book_store;

use book_store;


insert into Book values('978-873625125','Harry Potter','zhanghao','SUTD Press','2016',4,25.65,'paperback','novel','key1 key2 key3');
insert into Book values('978-873625123','Harry Potter','zhanghao','SUTD Press','2016',4,25.65,'paperback','novel','key1 key2 key3');
insert into User values('zhanghao','password','4567 7876 8876 9876','8 Somapah Rd','85359434',true);


select * from Book;

select * from User;

select * from Order_Detail;

select * from Orders;

insert into Orders values(1, 'zhanghao', '2015-09-26', 'shipped');

insert into Order_Detail values(1, '978-873625125Order_Detail');

insert into Shopping_Cart values(1, 'zhanghao', '978-873625125',4);

select * from Shopping_Cart;