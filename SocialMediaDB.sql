drop database if exists SOCIAL_MEDIA;
create database SOCIAL_MEDIA;
use SOCIAL_MEDIA;

CREATE TABLE EDUCATION (
    user_id INT,
    education VARCHAR(100),
    PRIMARY KEY (user_id, education),
    FOREIGN KEY (user_id) REFERENCES PROFILE(user_id) ON DELETE CASCADE ON UPDATE CASCADE
)

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

