create database book_store;

use book_store;

create table User
(username varchar(14) primary key,
 password varchar(12));
 
insert into User values('zhanghao','password');
insert into User values('foo','bar');

select * from User;

select * from pet;

select * from person;

DROP TABLE `book_store`.`User`;