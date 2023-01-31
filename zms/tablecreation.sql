CREATE DATABASE `zoo`;
CREATE TABLE `admin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `password` varchar(20) DEFAULT NULL,
  `phone_num` bigint DEFAULT NULL,
  `gender` varchar(45) NOT NULL,
  PRIMARY KEY (`id`,`user_id`)
);



CREATE TABLE `block` (
  `block_id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`block_id`)
);




CREATE TABLE `visitor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `age` varchar(10) DEFAULT NULL,
  `phone_num` bigint DEFAULT NULL,
  `date_of_visit` date DEFAULT NULL,
  `paid` int DEFAULT NULL,
  PRIMARY KEY (`id`)
);


CREATE TABLE `animals` (
  `animal_id` varchar(20) NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `gender` varchar(45) DEFAULT NULL,
  `date_of_join` date DEFAULT NULL,
  `b_id` int DEFAULT NULL,
  PRIMARY KEY (`id`,`animal_id`),
  UNIQUE KEY `animal_id_UNIQUE` (`animal_id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `b_id` (`b_id`),
  CONSTRAINT `b_id` FOREIGN KEY (`b_id`) REFERENCES `block` (`block_id`)
);



CREATE TABLE `adoption` (
  `a_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `amount` int DEFAULT NULL,
  `date_of_adoption` date DEFAULT NULL,
  `phone_num` bigint DEFAULT NULL,
  `an_id` varchar(20) NOT NULL,
  PRIMARY KEY (`a_id`),
  KEY `an_id_idx` (`an_id`),
  CONSTRAINT `an_id` FOREIGN KEY (`an_id`) REFERENCES `animals` (`animal_id`) ON DELETE CASCADE
);


CREATE TABLE `employee` (
  `e_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `salary` varchar(45) NOT NULL,
  `age` int DEFAULT NULL,
  `b_id` int DEFAULT NULL,
  `d_of_join` date NOT NULL,
  PRIMARY KEY (`e_id`),
  KEY `b_id` (`b_id`),
  CONSTRAINT `employee_ibfk_1` FOREIGN KEY (`b_id`) REFERENCES `block` (`block_id`)
);


insert into admin(user_id,name,password,phone_num,gender) values('guru123','GURURAJ','9844',8971260336,'MALE')


insert into block values(1,'BIRDS');
insert into block values(2,'CARNIVORE');
insert into block values(3,'PRIMATES');
insert into block values(1,'REPTILES');
insert into block values(1,'HERBIVORES');
insert into block values(1,'OMNIVORES');


