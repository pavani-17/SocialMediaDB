drop database if exists SOCIAL_MEDIA;
create database SOCIAL_MEDIA;
use SOCIAL_MEDIA;

DROP TABLE IF EXISTS USER;
CREATE TABLE USER (
    user_id INT NOT NULL AUTO_INCREMENT primary key,
    password varchar(120) NOT NULL,
    name varchar(50) NOT NULL,
    email varchar(20) NOT NULL,
    contact_address varchar(300) NOT NULL,
    phone int,
    uptime TIME not null
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

insert into USER VALUES(NULL, 'sdfsfs', 'NMAE',  'pb@afsd.com', 'voldem', 1231231, '12:12:21');

DROP TABLE IF EXISTS POST;
CREATE TABLE POST (
    post_id int not null AUTO_INCREMENT,
    time TIMESTAMP not null,
    text TEXT,
    media varchar(10000),
    PRIMARY KEY(post_id),
    user_id int not null,
    CONSTRAINT OWNS_POST FOREIGN KEY (user_id) REFERENCES USER (user_id) on DELETE CASCADE on UPDATE CASCADE,
    CONSTRAINT CONTENT_PRESENT_IN_POST CHECK (text is NOT NULL OR media is NOT NULL)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;


DROP TABLE IF EXISTS COMMENT;
CREATE TABLE COMMENT(
    comment_id int not null AUTO_INCREMENT PRIMARY KEY,
    time TIMESTAMP not NULL,
    text TEXT,
    media VARCHAR(10000),
    CONSTRAINT CONTENT_PRESENT_IN_COMMENT CHECK (text is NOT NULL OR media is NOT NULL)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

DROP TABLE IF EXISTS STORIES;
CREATE TABLE STORIES(
    story_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    time TIMESTAMP,
    text TEXT,
    media VARCHAR(10000),
    user_id int not null,
    CONSTRAINT OWNS_STORY FOREIGN KEY (user_id) REFERENCES USER (user_id) on DELETE CASCADE on UPDATE CASCADE,
    CONSTRAINT CONTENT_PRESENT_IN_STORY CHECK (text is NOT NULL OR media is NOT NULL)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;



DROP TABLE IF EXISTS MESSAGE;
CREATE TABLE MESSAGE(
    message_id int not null PRIMARY KEY AUTO_INCREMENT,
    text TEXT not null
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

DROP TABLE IF EXISTS PROFILE;
CREATE TABLE PROFILE (
    user_id int PRIMARY KEY,
    date_of_birth DATE not null,
    sex varchar(30),
    sexes ENUM('Male', 'Female', 'Others', 'PreferNotToSay'),
    CONSTRAINT OWNS_PROFILE FOREIGN KEY (user_id) REFERENCES USER (user_id) on DELETE CASCADE on UPDATE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8;
