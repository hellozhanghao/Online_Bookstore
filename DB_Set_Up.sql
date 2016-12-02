create database book_store;

use book_store;


insert into Book values('978-873625125','Harry Potter','zhanghao','SUTD Press','2016',4,25.65,'paperback','novel','key1 key2 key3');
insert into User values('admin','adminpass','credit_card','add','34534',true);


select * from Book;

select * from User;

select * from Order_Detail;

select * from Orders;

insert into Orders values(1, 'zhanghao', 354535, 'shipped', 4);