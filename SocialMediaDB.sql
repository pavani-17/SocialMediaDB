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

CREATE TABLE EDUCATION (
    user_id INT,
    education VARCHAR(100),
    PRIMARY KEY (user_id, education),
    FOREIGN KEY (user_id) REFERENCES PROFILE(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE PAGE (
    page_id int AUTO_INCREMENT NOT NULL PRIMARY KEY,
    page_name varchar(50) NOT NULL,
    owner_id int,
    FOREIGN KEY (owner_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE BUSINESS_PLACE (
    page_id int PRIMARY KEY,
    owner_name varchar(50) NOT NULL,
    location varchar(100),
    FOREIGN KEY (page_id) REFERENCES PAGE(page_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE PROD_BP(
    page_id int,
    prod_name varchar(50),
    prod_price decimal(10,2),
    FOREIGN KEY (page_id) REFERENCES BUSINESS_PLACE(page_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(page_id,prod_name,prod_price)
);

CREATE TABLE COMPANY (
    page_id int PRIMARY KEY,
    work_domain varchar(30),
    FOREIGN KEY (page_id) REFERENCES PAGE(page_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE BRANCH_COMPANY (
    page_id int,
    branch varchar(50),
    FOREIGN KEY (page_id) REFERENCES COMPANY(page_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (page_id, branch)
);

CREATE TABLE BRAND_PRODUCT (
    page_id int PRIMARY KEY,
    website varchar(50),
    cust_service int(10),
    FOREIGN KEY (page_id) REFERENCES PAGE(page_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE PUBLIC_FIGURE (
    page_id int PRIMARY KEY,
    celeb_name varchar(50),
    celeb_field varchar(50),
    FOREIGN KEY (page_id) REFERENCES PAGE(page_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE NEWS_PUB_FIG (
    page_id int ,
    news varchar(1000),
    published_time timestamp,
    FOREIGN KEY (page_id) REFERENCES PUBLIC_FIGURE(page_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (page_id,published_time)
);

CREATE TABLE ENTERTAINMENT  (
    page_id int PRIMARY KEY,
    events varchar(300),
    audience varchar(300),
    FOREIGN KEY (page_id) REFERENCES PAGE(page_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE CAUSE_COMMUNITY  (
    page_id int PRIMARY KEY,
    goal varchar(300),
    activities varchar(300),
    FOREIGN KEY (page_id) REFERENCES PAGE(page_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE SOCIAL_MEDIA.GROUP (
    group_id int AUTO_INCREMENT PRIMARY KEY,
    group_name varchar(50) NOT NULL,
    group_privacy ENUM('Public', 'Private', 'Secret')
);