create database book_store;

use book_store;

create table User
(username varchar(14) primary key,
 password varchar(12));
 
insert into User values('zhanghao','password');
insert into User values('foo','bar');

select * from User;


DROP TABLE `book_store`.`User`;


insert into Book values('978-873625125','Harry Potter','zhanghao','SUTD Press','2016',4,25.65,'paperback','novel','key1 key2 key3');
insert into User values('admin','adminpass','credit_card','add','34534',true)


select * from Book;